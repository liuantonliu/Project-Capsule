// var myJSON;
var stored = "";

function getValue() {
    var x = document.getElementById('input1').value;
    if (stored == ""){
        for (var i=1;i<9;i++){
            newcard(x,i);
            // setTimeout(function() { alert(i) }, 1000*(i+1));
        }
        stored = x;
    }else if(x != stored){
        var col_wrapper = document.getElementById("grid-container").getElementsByTagName("div");
        var len = col_wrapper.length;

        for (var i = 0; i < len; i++) {
            if (col_wrapper[0].className.toLowerCase() == "grid-item") {
                col_wrapper[0].parentNode.removeChild(col_wrapper[0]);
            }
        }
        for (var i=1;i<9;i++){
            newcard(x,i);
            // setTimeout(function() { alert(i) }, 1000*(i+1));
        }
        stored = x;
    }
    
    
    // var y = document.getElementById('boo');
    // $.post( "/postmethod", {
    //     canvas_data: JSON.stringify(x)
    //   }, function(err, req, resp){
    //     window.location.href = "/results/"+resp["responseJSON"]["uuid"];  
    //   });
    // window.location.href = "http://127.0.0.1:5500/interface.html/query_example?language=" + x;
    // var mylink = "http://127.0.0.1:5500/interface.html/query_example?language=" + x;
    // alert(mylink);
    //= "http://website.com/page.aspx?list=" + a + "&sublist=" + b;
    // y.innerHTML=x;
    // myJSON = JSON.stringify(x);
    // alert(myJSON);
  }


function newcard(x,i){
    

    var block_to_insert ;
    var container_block ;
    var wardoresize = 4;

    var res = "clothing #" + i.toString();
    
    block_to_insert = document.createElement( 'div' );
    block_to_insert.innerHTML = 'Clothing #' + i.toString() ;
    block_to_insert.setAttribute("class","grid-item");
    block_to_insert.setAttribute("id",res )
    
    container_block = document.getElementById( 'grid-container' );
    container_block.appendChild( block_to_insert );
    
    var img = document.createElement("img");
    var src = document.getElementById(res);
    img.src = "pic/fashion/"+x+i+".jpg";
    src.appendChild(img);
    document.getElementById(res).width = "10px";
}
 