docker-machine start default
eval $(docker-machine env default)
docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash
docker-machine ip default

scrapy shell 'http://192.168.99.100:8050/render.html?url=http://foe.mmu.edu.my/v3/main/staff/staff_directory.php?page=1&wait=0.5'



scrapy shell 'http://192.168.99.100:8050/render.html?url=http://goog&wait=0.5'
