import os
import logging
this_dir = os.path.dirname(os.path.abspath(__file__))

logging.info('Installing GNG')

os.chdir(this_dir+'/code/dotnetcore/GNG')
os.system('dotnet build --configuration Release')
os.chdir(this_dir)

logging.info('Installing ConnectedComponents')

os.chdir(this_dir+'/code/dotnetcore/ConnComponents')
os.system('dotnet build --configuration Release')
os.chdir(this_dir)

logging.info('Installing Clustering')

os.chdir(this_dir+'/code/dotnetcore/AgglomerativeClustering/')
os.system('dotnet build --configuration Release')
os.chdir(this_dir)

logging.info('Installing GNG')

os.chdir(this_dir+'/code/dotnetcore/GNG')
os.system('dotnet build --configuration Release')
os.chdir(this_dir)

logging.info('Installing ConnectedComponents')

os.chdir(this_dir+'/code/dotnetcore/ConnComponents')
os.system('dotnet build --configuration Release')
os.chdir(this_dir)

logging.info('Installing Clustering')

os.chdir(this_dir+'/code/dotnetcore/AgglomerativeClustering/')
os.system('dotnet build --configuration Release')
os.chdir(this_dir)

logging.info('Installation of GNG is complete!')