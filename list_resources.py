#!/usr/bin/python3

# lists available visa resources

import visa

rm=visa.ResourceManager('@py')
resources=rm.list_resources()
print(resources)

#for resource in resources:
#    
