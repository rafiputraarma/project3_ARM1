$(document).ready(function () {
  selesai();
});

var myArrayturbin = [];

function selesai() {
  setTimeout(function () {
    update();
    buildTableturbin(myArrayturbin);
    selesai();
  }, 3000);
}

//fungcion update
function update() {
  $.ajax({
    url: "/turbin",
    data: "rvturbin",
    dataType: "JSON",
    type: "GET",
    success: function (data) {
      myArrayturbin = data.rvturbin;
      console.log(data);
    },
  });
}

//motor----
function buildTableturbin(data) {
  var table = document.getElementById("myturbin");
  $("#myturbin").empty();

  for (var i = 0; i < data.length; i++) {
    var event_data = "";

    event_data += "<tr>";
    event_data += "<td>" + (i + 1) + "</td>";
    event_data += "<td>" + data[i].datetime + "</td>";
    event_data += "<td>" + data[i].temp_inlet + "</td>";
    event_data += "<td>" + data[i].temp_outlet + "</td>";
    event_data += "<td>" + data[i].pressure_inlet + "</td>";
    event_data += "<td>" + data[i].pressure_outlet + "</td>";
    event_data += "<td>" + data[i].status + "</td>";

    event_data += "</tr>";
    $("#myturbin").append(event_data);
  }
}
