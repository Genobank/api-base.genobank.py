console.log(window.test)

function init(){
  if (window.test){
    $("#navbar").css("background-color", "#FF766B");
    $("#profiles-href").attr("href","/adminpage/test-profile")
    $("#permette-href").attr("href","/adminpage/test-permittee")
  }
  else{
    $("#navbar").css("background-color", "#EAEFF4");
    $("#profiles-href").attr("href","/adminpage/profile")
    $("#permette-href").attr("href","/adminpage/permittee")
  }
}
