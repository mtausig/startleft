import logging

from http import HTTPStatus

from fastapi import APIRouter, File, UploadFile, Form, Response

from startleft.api.controllers.iac.iac_type import IacType
from startleft.api.error_response import ErrorResponse
from startleft.messages import messages
from startleft.project.otm_project import OtmProject

PREFIX = '/api/v1/startleft/iac'
URL = ''
RESPONSE_STATUS_CODE = HTTPStatus.CREATED

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=PREFIX,
    tags=["IaC"],
    responses={
        201: {"description": messages.OTM_SUCCESSFULLY_CREATED},
        400: {"description": messages.BAD_REQUEST,
              "model": ErrorResponse},
        401: {"description": messages.UNAUTHORIZED_EXCEPTION,
              "model": ErrorResponse},
        403: {"description": messages.FORBIDDEN_OPERATION,
              "model": ErrorResponse},
        'default': {"description": messages.UNEXPECTED_API_ERROR,
                    "model": ErrorResponse}
    }
)


@router.post(URL, status_code=RESPONSE_STATUS_CODE, description="Generates an OTM threat model from an IaC file")
def iac(iac_file: UploadFile = File(..., description="File that contains the Iac definition"),
        iac_type: IacType = Form(..., description="Type of IaC File: CLOUDFORMATION"),
        id: str = Form(..., description="ID of the new project"),
        name: str = Form(..., description="Name of the new project"),
        mapping_file: UploadFile = File(..., description="File that contains the mapping between IaC "
                                                         "resources and threat model resources.")):
    logger.info(f"POST request received for creating new project with id {id} and name {name} from IaC {iac_type} file")

    logger.info("Parsing IaC file to OTM")
    otm_project = OtmProject.from_iac_file_to_otm_stream(id, name, iac_type, [iac_file.file]
                                                         , [mapping_file.file] if mapping_file else [])

    return Response(status_code=201, media_type="application/json", content=otm_project.get_otm_as_json())
