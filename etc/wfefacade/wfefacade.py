import argparse
import json
import pickledb
import requests
import threading
import time

from flask import Flask, request, make_response

app = Flask(__name__)

apiKey = None
easemlAddr = None
db = pickledb.load("id_mappings.db", True)


def run_get_query(url, params=None):
    params = params or {}
    result = []
    r = requests.get(url, params, headers={"X-API-KEY" : apiKey})
    if r.status_code == 200:
        r_json = r.json()
        result = r_json["data"]

        cursor = r_json["metadata"]["next-page-cursor"]
        if cursor != "":
            rec_result = run_get_query(url, dict(params, **{"cursor" : cursor}))
            result.append(rec_result)
    
    else:
        raise RuntimeError(r_json["error"])
    
    return result


# Base dummy route to test the connection.
@app.route("/")
def hello():
    response = {"message": "Hello World!"}
    return json.dumps(response)


# Submit a new job to easeml.
@app.route("/ras/training_service", methods=["POST"])
def submit_job():
    assert request.method == "POST"

    # Parse arguments from the request body.
    execution_id = request.json["executionId"]
    execution_name = request.json["executionName"]
    input_paras = request.json["inputParas"]
    exec_id = "%s/%s" % (execution_id, execution_name)
    print("New job submission " + exec_id)
    print("Params:")
    print(json.dumps(input_paras, indent=2))

    # TODO: This part will change. The dataset ID will be some path to a dataset in an external database.
    dataset_id = input_paras["datasetId"]

    # TODO: Here we will load the dataset into easeml. Now we assume the dataset is already loaded.

    # Get dataset object.
    r = requests.get("http://" + easemlAddr + "/api/v1/datasets/" + dataset_id, headers={"X-API-KEY" : apiKey})
    r_json = r.json()
    if r.status_code != 200:
        error_resp = {"Error" : "JOB_SUBMISSION_ERROR", "error_desc" : r_json["error"]}
        return make_response(json.dumps(error_resp), 500)
    schema_in = r_json["data"]["schema-in"]
    schema_out = r_json["data"]["schema-out"]

    # Get models that comform to the schema.
    try:
        models = run_get_query("http://" + easemlAddr + "/api/v1/modules", {"type" : "model", "schema-in" : schema_in, "schema-out" : schema_out})
    except:
        error_resp = {"Error" : "JOB_SUBMISSION_ERROR"}
        return make_response(json.dumps(error_resp), 500)
    model_ids = [m["id"] for m in models]

    # Create an easeml job.
    job_request_body = {
        "dataset" : dataset_id,
        "models" : model_ids,
        "config-space" : "",
        "objective" : "root/objective1",             # TODO: Hardcode an objective here or accept parameter.
        "max-tasks" : 100
    }
    r = requests.post("http://" + easemlAddr + "/api/v1/jobs",
        data=json.dumps(job_request_body), headers={"X-API-KEY" : apiKey})
    
    # Construct response.
    if r.status_code == 201:

        # Record the new job ID in a data storage and associate it with execution_id and execution_name.
        job_id = r.headers["Location"].split("/")[-1]
        print("New job ID: %s" % job_id)
        

        # Get the job object.
        r = requests.get("http://" + easemlAddr + "/api/v1/jobs/" + job_id, headers={"X-API-KEY" : apiKey})
        r_json = r.json()

        if r.status_code == 200:
            # If everything went well, we can cache the job object.
            job_obj = r_json["data"]
            db.set(exec_id, {"id" : job_id, "obj" : job_obj } )
            return make_response("OK", 200)
        else:
            error_resp = {"Error" : "JOB_SUBMISSION_ERROR", "error_desc" : r_json["error"]}
            return make_response(json.dumps(error_resp), 500)
        
    else:
        r_json = r.json()
        error_resp = {"Error" : "JOB_SUBMISSION_ERROR", "error_desc" : r_json["error"]}
        return make_response(json.dumps(error_resp), 500)


# Get status info about a JOB.
@app.route("/ras/training_service/<execution_id>/<execution_name>", methods=["GET"])
def get_job_info(execution_id, execution_name):
    assert request.method == "GET"

    # We return the cached job info.
    exec_id = "%s/%s" % (execution_id, execution_name)
    v = db.get(exec_id)

    job_obj = v["obj"]

    job_status = job_obj["status"]
    job_status_map = {
        "scheduled" : "inprogress",
        "running" : "inprogress",
        "pausing" : "inprogress",
        "paused" : "inprogress",
        "resuming" : "inprogress",
        "completed" : "success",
        "terminating" : "failed",
        "terminated" : "failed",
        "error" : "failed",
    }
    job_status = job_status_map[job_status]

    resp = {
        "id" : exec_id,
        "status" : job_status
    }
    
    return make_response(json.dumps(resp), 200)


# Terminate a JOB.
@app.route("/ras/training_service/<execution_id>/<execution_name>", methods=["DELETE"])
def terminate_job(execution_id, execution_name):
    assert request.method == "DELETE"

    exec_id = "%s/%s" % (execution_id, execution_name)
    v = db.get(exec_id)
    job_id = v["id"]

    r = requests.patch("http://" + easemlAddr + "/api/v1/jobs/" + job_id, data={"status" : "terminating"}, headers={"X-API-KEY" : apiKey})

    if r.status_code == 200:

        # This is not safe to do. Potential race condition.
        v["obj"]["status"] = "terminating"
        db.set(exec_id, v)

        return make_response("OK", 200)

    else:
        r_json = r.json()
        error_resp = {"Error" : "JOB_DELETION_ERROR", "error_desc" : r_json["error"]}
        return make_response(json.dumps(error_resp), 500)


def update_job_cache():

    while True:
        try:
            jobs = run_get_query("http://" + easemlAddr + "/api/v1/jobs")
            jobs_dict = {job["id"] : job for job in jobs}
            
            for exec_id in db.getall():
                v = db.get(exec_id)
                job_id = v["id"]

                # TODO: Check if the status has changed. If yes send a message to the workflow engine.

                job_obj = jobs_dict[job_id]
                db.set(exec_id, {"id" : job_id, "obj" : job_obj } )

        except:
            pass
        
        time.sleep(1)

easemlAddr = "localhost:8080"
apiKey = "2f0b74a0-191b-4668-a956-b151d24ff3a2"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Facade to the easeml REST API.")
    parser.add_argument("--easeml-addr", type=str, default="localhost:8080", required=False,
        help="Address of the easeml controller service.")
    parser.add_argument("--api-key", type=str, required=False,
        help="API key to access the easeml service REST API.")
    args = parser.parse_args()

    apiKey = args.api_key
    easemlAddr = args.easeml_addr

    apiKey = "2f0b74a0-191b-4668-a956-b151d24ff3a2"

    updater_thread = threading.Thread(target=update_job_cache)
    updater_thread.start()

    app.run(debug=True)
