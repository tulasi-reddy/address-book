from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal, session
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.responses import JSONResponse
from logging.config import dictConfig
import logging

dictConfig(schemas.LogConfig().dict())
logger = logging.getLogger("addressbook")


app = FastAPI()


models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# ********************************* INSERT ADDRESS ********************************* #

@app.post('/address', status_code=status.HTTP_201_CREATED)
def insert_address(request:schemas.Address, response : Response, db : Session = Depends(get_db)):
    """
        This api is used to add new address details\n

        Parameters:\n
        
        {\n
            address_line_one (str) : address line 1 (door no. / flat no.)\n
            address_line_two (str) : address line 2 (street number / building name/ apartment name)\n
            address_line_three (str) : address line 3 (road name, district)\n
            city_name (str) : Name of the city where the person resides\n
            state_name (str) : Name of the state where the person resides\n
            pin_code (str) : Pincode of the area where he stays\n
            is_current_address (bool) : It a boolean value which indicates whether the given address is whether current address or no\n
            land_mark (str) : Any place near to his/her address which can be easily seen and recognized from a distance\n
            latitude (float) : Measurement of distance north or south of the Equator (to point address)\n
            longitude (float) : The measurement east or west of the prime meridian (to point address)\n
        }\n
        
        
        sample data : \n
        {\n
            "address_line_one": "Shop No 2",
            "address_line_two": "Rameshghar, T.h.kataria Marg,",
            "address_line_three": "Matunga (west)",
            "city_name": "Mumbai"
            "state_name": "Maharashtra",
            "pin_code": "400016",
            "land_mark": "near gandhi circle",
            "latitude": 13.001159,
            "longitude": 77.748224
        }\n
        
        Returns: \n
        dict: Newly created address details are fetched as response

    """
    try:
        new_address = models.Address(address_line_one = request.address_line_one,address_line_two = request.address_line_two,
                                    address_line_three = request.address_line_three,city_name = request.city_name,
                                    state_name = request.state_name,pin_code = request.pin_code, land_mark = request.land_mark,
                                    latitude = request.latitude, longitude = request.longitude)
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        response.status_code = status.HTTP_201_CREATED
        logger.info("New address details added to database successfully")
        return {'address_details' : new_address}
    
    except Exception as ex: 
        logger.error(f"Exception encountered while adding new address details : {ex}")
        return JSONResponse (status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,content = {"message": f"Exception encountered : {ex}"})
        
        
# ------------------------------------- END ------------------------------------- #     
        
# ********************************* DELETE ADDRESS ********************************* #       
    
@app.delete('/address/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_address_by_id(id, response : Response, db : Session = Depends(get_db)):
    """
        This api is used to delete address details by address id \n

        Parameters: \n
        id (int) : address 'id' to be deleted \n
        
        Returns: \n
        dict: message would be displayed either related to success or failure  

    """
    try:
        address = db.query(models.Address).filter(models.Address.id == id)
        
        if address.count() < 1:
            return JSONResponse (status_code = status.HTTP_204_NO_CONTENT, content = {"message": "Address with the id does not exist"})
        address.delete(synchronize_session=False)
        db.commit()
        logger.info(f"Address details with id : {id} deleted succesfully")
        response.status_code = status.HTTP_200_OK
        return {'details' : f"Address details with id : {id} deleted succesfully"}
     
    except Exception as ex: 
        logger.error(f"Exception encountered while deleting address details by Id : {ex}")
        return JSONResponse (status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,content = {"message": f"Exception encountered : {ex}"})
        
# ------------------------------------- END ------------------------------------- #     


# ********************************* UPDATE ADDRESS ********************************* #       

@app.put('/address/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_address_by_id(id, request : schemas.Address , response : Response,db : Session = Depends(get_db)):
    """
        This api is used to add new address details \n

        Parameters: \n
        id (int) : Id of the address that needs to be updated\n
        request body: \n
            # sample input data \n
            {
                "address_line_one": "64/3",\n
                "address_line_two": "Ok Road",\n
                "address_line_three": "Next To Telegraph Office, Ragi Pet",\n
                "city_name": "Bangalore",\n
                "state_name": "Karnataka",\n
                "pin_code": "560002",\n
                "land_mark": "canara bank",\n
                "latitude": 12.962559,\n
                "longitude": 77.709624\n
            } \n
        Returns: \n
        dict: Newly created address details are fetched as response

    """
    try:  
        address = db.query(models.Address).filter(models.Address.id == id)
        if address.count() < 1:
            return JSONResponse (status_code = status.HTTP_204_NO_CONTENT, content = {"message": "Address with the id does not exist"})
        address.update(request.dict())
        db.commit()
        logger.info(f"Address details with id : {id} updated succesfully")
        response.status_code = status.HTTP_200_OK
        return {'details' : f"Address details with id : {id} updated succesfully"}
     
    
    except Exception as ex: 
        logger.error(f"Exception encountered while updating address details by Id : {ex}")
        return JSONResponse (status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,content = {"message": f"Exception encountered : {ex}"})
        

# ------------------------------------- END ------------------------------------- #     

# ********************************* FETCH ALL ADDRESSES ********************************* #       

@app.get('/address')
def fetch_all_addresses(db : Session = Depends(get_db)):
    """
        This api is used to fetch all address details \n

        Parameters: \n
        No paramenters required \n
        
        Returns: \n
        list: All the address details are fetched as response

    """
    try: 
        addresses =  db.query(models.Address).all()
        logger.info(f"All address details fetched succesfully")
        return addresses
    
    except Exception as ex: 
        logger.error(f"Exception encountered while fetching all address details : {ex}")
        return JSONResponse (status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,content = {"message": f"Exception encountered : {ex}"})
        
# ------------------------------------- END ------------------------------------- #     

     
# ********************************* FETCH ADDRESS DETAILS BY ID ********************************* #       

@app.get('/address/{id}', status_code=200)
def fetch_address_by_id(id, response : Response, db : Session = Depends(get_db)):
    """
        This api is used to add new address details

        Parameters: \n
        id (int) : Id of the address that needs to be fetched\n
        
        
        Returns: 
        dict: Address details are fetched as response

    """
    address = db.query(models.Address).filter(models.Address.id == id).first()
    if not address:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'details' : f"Address details between does not exist"}
    
    logger.info(f"Address details by id fetched succesfully")
    return address

# ------------------------------------- END ------------------------------------- #     


# ********************************* FETCH ADDRESS DETAILS BY CO-ORDINATES ********************************* #       

@app.get('/address_by_coordinates/', status_code=200)
def fetch_address_details_by_coordinates(latitude, longitude, distance, response : Response, db : Session = Depends(get_db)):
    """
        This api is used to add new address details \n

        Parameters: \n
        distance (int) : Distance radius \n
        latitude (float) : Measurement of distance north or south of the Equator (to point address) \n
        longitude (float) : The measurement east or west of the prime meridian (to point address) \n
        
        Sample data: \n
        Positive test case: { \n
            distance : 500 \n
            latitude : 12.961359 \n
            longitude : 77.708424 \n
        } \n
        
        Negative test case:{ \n
            distance : 50 \n
            latitude : -12.961359 \n
            longitude : -77.708424 \n
        }
        Returns: \n
        list: Address details are fetched as response based on given inputs

    """
    try: 
        stmt = text("""select * from Address where (latitude - :startlat)*(latitude - :startlat) + (longitude-:startlng)*(longitude-:startlng) <  (:distance/111)*(:distance/111)""")
        result = session.query(models.Address).from_statement(stmt).params(startlat=latitude, startlng=longitude,distance=distance).all()
        if len(result) < 1:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'details' : f"Address details between latitude {latitude} and logitude {longitude} with distance {distance} does not exist"}
        logger.info(f"Address details by co-ordinates fetched succesfully")
        return result
    
    except Exception as ex: 
        logger.error("Exception encountered while deleting address details by Id : {ex}")
        return JSONResponse (status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,content = {"message": f"Exception encountered : {ex}"})
        
    # select * from Address where (latitude - 12.961359)*2 + (longitude-77.708424)*2 < (500/111)*2
    # select * from Address where (latitude - 12.961359)*2 + (longitude-77.708424)*2 <  (50/111)*2

# ------------------------------------- END ------------------------------------- #     
