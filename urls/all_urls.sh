for BASE in `cat 500_views.txt`
do
   URL=`echo ${BASE} | sed -e s/HOST/ALB-two-simple-instances-735948120.us-east-2.elb.amazonaws.com/`
   VIEW=`echo ${BASE} | sed -e 's/.*pov=//' -e 's/\(view[0-9][0-9]\).*/\1/'`
   echo ${URL}
   echo ${VIEW}
   DATA=`curl ${URL}`
   echo ${DATA}
done
