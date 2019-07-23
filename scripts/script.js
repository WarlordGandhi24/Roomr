let submit = document.querySelector("#pref")
let pfp = document.querySelector("#pfp")
pfp.addEventListener('click', ()=>{
  pfp.src = "https://www.setaswall.com/wp-content/uploads/2017/07/Black-Wallpapers-25-1920-x-1200.jpg";
})

$("#profileImage").click(function(e) {
    $("#imageUpload").click();
});

function fasterPreview( uploader ) {
    if ( uploader.files && uploader.files[0] ){
          $('#profileImage').attr('src',
             window.URL.createObjectURL(uploader.files[0]) );
    }
}

$("#imageUpload").change(function(){
    fasterPreview( this );
});
