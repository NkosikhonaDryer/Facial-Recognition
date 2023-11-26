let countdown;
let seconds = 30;
const videoElement = document.getElementById('videoStream');
const ModeHolder = document.getElementById('ModeHolder')

function startCountdown() {

    console.log("seconds: ",seconds)
    currentLength = 0
    modeId = 0
    count = 5
    setInterval(function() {
        seconds--;

        if (seconds < 0) {
            clearInterval(countdown);
            console.log( 'Times up!');
        } else {

            //getting module

            fetch("{% url 'getMessages' classId=class.ClassId %}",{
                method:"GET",
                
            
                
                
            }).then(function(response){
                
                return response.json();
                
            }).then(function (json){
                console.log("Messages", json)
                
                if(json.currentAttendee){
                    if(json.currentAttendee >modeId ){
                        console.log("new mode found")
                        modeId = json.currentAttendee
                        count = 5
                        videoElement.src = "";
                        videoElement.hidden = true

                        ModeHolder.hidden = false
                        ModeHolder.classList.add = 'text-'+json.type
                        messageHolder = document.getElementById("messageHolder")
                        messageHolder.innerHTML = json.Message
                    }
                    console.log("Mode found")
                    counter = document.getElementById("counter")
                    counter.innerHTML = count--
                    if (count == 0){
                        removeMode()
                        ModeHolder.hidden = true
                        messageHolder = document.getElementById("messageHolder")
                        messageHolder.innerHTML = ''
                        
                        videoElement.src = "{% url 'video_feed' classId=class.ClassId %}";
                        videoElement.hidden = false
                    }
                }
                else{
                    console.log("No mode!")
                    
                    
                }
            })




            //Adding Attendance
            seconds++
            console.log( 'Times: ',seconds);
            fetch("{% url 'allAttendees' classID=class.ClassId %}",{
                method:"GET",
                
            
                
                
            }).then(function(response){
                
                return response.json();
                
            }).then(function (json){

                domain = document.getElementById("domain")
                if(json.length > currentLength){
                    for(var i=0; i< json.length; i++){
                        AttendanceHolder = document.getElementById("AttendanceHolder")
                        AttendanceHolder.innerHTML += '<div class="col-xl-3 col-md-6 mb-4">'+

                            '<div class="card border-left-primary shadow h-100 py-2">'+
                                '<div class="card-body">'+
                                    '<div class="row no-gutters align-items-center" style="display:flex;justify-content:center">'+
                                        '<img id="" style="width:inherit; width:100%;border:solid;max-height:320px"  src="http://'+domain.value +'/'+json[i].StudentIamge +'"/>'+
                                    '</div>'+
                                    '<div class="row no-gutters align-items-center">'+
                                        '<div class="col mr-2">'+
                                            '<div class="text-xs font-weight-bold text-info text-uppercase mb-1">'+
                                                ''+json[i].first_name+' '+json[i].last_name+'</div>'+
                                            '<div class="h5 mb-0 font-weight-bold text-gray-800"></div>'+
                                        '</div>'+
                                        
                                    '</div>'+
                            
                                '</div>'+
                            '</div>'+



                            '</div>'
                        console.log("Data: ", json[i].StudentIamge)
                    }
                }
                currentLength = json.length

                console.log("current Length: ", currentLength)
                
                
            })
                
        }
    }, 1000); 
}

startCountdown()



function removeMode(){
    fetch("{% url 'removeMode' classId=class.ClassId %}",{
        method:"GET",
        
    
        
        
    }).then(function(response){
        
        return response.json();
        
    }).then(function (json){
        console.log("Js", json)
        
    })
}
