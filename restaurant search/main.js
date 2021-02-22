let marker = [];

//close-iconをクリック
$(document).on('click', '.close-icon', function(){
  $(".details").removeClass("active");
  $(".details").addClass("hidden");
  console.log("hello");
});
//クリックしたらfreewordを代入
function  searchclick(event) {
  const freeword= $('#freeword').val();
  searchRest(freeword);
  marker.forEach(function (marker, index) { marker.setMap(null); });
  event.preventDefault();
}



const restList =  new Vue({
  el: '#restlist',
  data: {
    informations: [],
  },
  created() {
  },
});

const detail =  new Vue({
  el: '#detail',
  data: {
    currentInfo:{},
  },
  created() {
  },
});


function searchRest(freeword){
  $("section").removeClass("hidden");

  $('#restlist').waitMe({
    effect : 'bounce',
    text : '',
    maxSize : '',
    waitTime : -1,
    textPos : 'vertical',
    fontSize : '',
    source : '',
    onClose : function() {}
  });



  /*  if (data.stat !== 'ok') {
      return;
    }*/
  
  // 整形の参考
  // const animalPhotos = data.photos.photo.map(photo => ({
  //   id: photo.id,
  //   imageURL: getFlickrImageURL(photo, 'q'),
  //   pageURL: getFlickrPageURL(photo),
  //   text: getFlickrText(photo),
  // }));
    const keyid = "b232c23fcd8f6d5bac50bc28d09bb9e1"; 
    const hit_per_page = 10;
    const range = 5;
    const url = `https://api.gnavi.co.jp/RestSearchAPI/v3/?keyid=${keyid}&freeword=${freeword}&hit_per_page=10`;
    $.getJSON(url, (data) => {
    
      
      console.log(data);
      console.log(data.rest[1].name);
      
      
      // dataを使って、ピンをふらせる
      /* for(i = 0; i < hit_per_page; i++){
        let marker = new google.maps.Marker({
          position:{lat: parseFloat(data.rest[i].latitude), lng: parseFloat(data.rest[i].longitude)},
          map:map
        });*/
      
      const details =  data.rest.map(information => ({
        name:information.name,
        address:information.address,
        tel:information.tel,
        opentime:information.opentime,
        holiday:information.holiday,
        access:information.access.station
      }));  
        
      for (let i = 0; i < hit_per_page; i++) {
        
        markerLatLng = new google.maps.LatLng({lat: parseFloat(data.rest[i].latitude), lng: parseFloat(data.rest[i].longitude)}); // 緯度経度のデータ作成
        marker[i] = new google.maps.Marker({ // マーカーの追加
          position: markerLatLng, // マーカーを立てる位置を指定
          map: map // マーカーを立てる地図を指定
        });
        
        marker[i].addListener('click', function() { 
          $(".details").removeClass("hidden");
          $(".details").addClass("active");
          console.log("くりっくしました");
          console.log(details[i]);
        
          detail.currentInfo = details[i]; 
        
          /*detailsList.informations = data.rest.map(information => ({
            name:information.name,
            address:information.address,
            tel:information.tel,
            opentime:information.opentime,
            holiday:information.holiday,
            access:information.access
          }));    */    
        });
      }
      // このデータをvueで作っておいたリスト領域にデータを反映させる
      // listArea = new Vue ...
      // listArea.stores = オブジェクトの配列を代入。少し整形。
      restList.informations = data.rest.map(information => ({
        name:information.name,
        pageURL:information.url,
        imageURL:information.image_url.shop_image1
      }));
    
      $('#restlist').waitMe('hide');  
    
    });
}

window.onload = function() {
  const spinner = document.getElementById('loading');
  spinner.classList.add('loaded');
};

// $('#restlist').waitMe({
//   effect : 'win8',
//   text : 'Please wait...',
//   bg : false,
//   color : 000,
//   maxSize : '40',
//   waitTime : 3000,
//   textPos : 'vertical',
//   fontSize : '18px',
//   source : 'url',
//   onClose : function(event, el){}
// });



// // /**
// * -------------
// * Vueインスタンス
// * -------------
// */

// new Vue({
//   el: '#gallery',
//   data: {
//     photos: [],
//   },
//   created() {
//     this.apiSearch('cat');
//   },
//   methods: {
//       });
//     },
//   }});






// function gnaviFreewordSearch(hit_per_page){
//   var req = new XMLHttpRequest();
//   var keyid = "b232c23fcd8f6d5bac50bc28d09bb9e1";  
//   var freeword = document.forms.mainform.elements['freeword'].value;
//   var url = `https://api.gnavi.co.jp/RestSearchAPI/v3/?keyid=${keyid}&freeword=${freeword}&hit_per_page=${hit_per_page}`;
  
//   req.responseType = 'json';
  
//   req.open('GET', url, true);

//   req.onload = function(){
//     console.log(req.response.rest.name);
//   };
//   req.send();
// }

