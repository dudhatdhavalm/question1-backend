from fastapi import FastAPI, HTTPException
from enum import Enum
from typing import List, Dict, Any
import json
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class WorkflowOptions(str, Enum):
    workflow_1 = "workflow_1", "Workflow 1"
    workflow_2 = "workflow_2", "Workflow 2"
    workflow_3 = "workflow_3", "Workflow 3"

    def __new__(cls, key, value):
        obj = str.__new__(cls, [key])
        obj._value_ = key
        obj.full_name = value
        return obj

class ExecuteRequest(BaseModel):
    workflow_key: WorkflowOptions
    parameters: Dict[str, Any]

class ExecuteResponse(BaseModel):
    type: str
    value: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)


with open("workflows.json") as file:
    workflows = json.load(file)


@app.get("/workflow", response_model=List[Dict[str, str]])
def get_workflow() -> List[Dict[str, str]]:
    dropdown_values = [{"key": option.value, "value": option.full_name} for option in WorkflowOptions]
    return dropdown_values


@app.get("/description/{workflow_key}", response_model=Dict[str, Any])
def get_description(workflow_key: WorkflowOptions) -> Dict[str, Any]:
    workflow_data = workflows.get(workflow_key.value)
    if not workflow_data:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow_data

@app.post("/execute", response_model=List[ExecuteResponse])
def execute_workflow(request: ExecuteRequest) -> List[ExecuteResponse]:
    workflow_key = request.workflow_key
    parameters = request.parameters

    results = []

    if workflow_key == WorkflowOptions.workflow_1:
        results.append({"type": "text", "value": f"Executing Workflow 1 with params: {parameters}"})
        results.append({"type": "image", "value": "https://images.unsplash.com/photo-1613616631374-121ea711cc3d?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"})

    elif workflow_key == WorkflowOptions.workflow_2:
        results.append({"type": "text", "value": f"Executing Workflow 2 with params: {parameters}"})
        results.append({"type": "image", "value": "https://images.unsplash.com/photo-1613616631374-121ea711cc3d?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"})

    elif workflow_key == WorkflowOptions.workflow_3:
        results.append({"type": "text", "value": f"Executing Workflow 3 with params: {parameters}"})
        results.append({"type": "image", "value": "https://images.unsplash.com/photo-1542744173-05336fcc7ad4?q=80&w=2002&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"})

    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)