# pinkboto

A Colorful AWS SDK wrapper for Python

## Install
    
    pip install pinkboto

## Usage
    
    import pinkboto
    aws = pinkboto.aws(profile='production', region='us-east-1') 
    selector = {'resource': 'aws_db_instance'}
    projection = ['DBInstanceIdentifier', 'Endpoint']
    rds = aws.find(selector, projection)
    
#### Caching
By default, pinkboto caching all requests with 120 seconds lifespan. 

To disable:
    
    aws = pinkboto.aws(profile='production', region='us-east-1', cache=False)
    
To modify lifespan to 1 hour:

    aws = pinkboto.aws(profile='production', region='us-east-1', cache=3600)

#### Subfield projection
You can access a subfield in projection. For example 'Endpoint.Address' in rds 
    
    rds = aws.find({'resource': 'aws_db_instance'}, ['Endpoint.Address', 'AvailabilityZone'])

#### CSV output
    
    pinkboto.to_csv(rds, 'result.csv')

## Contributing
Pull requests for new features, bug fixes, and suggestions are welcome!

## License
GNU General Public License v3 (GPLv3)

