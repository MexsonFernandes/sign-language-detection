import { Component } from '@angular/core';
import { Camera, CameraOptions } from '@ionic-native/camera/ngx';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { LoadingController, ToastController } from '@ionic/angular';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  loading :any;

  home_image = '/assets/home.png';
  constructor(
    private camera: Camera,
    private httpClient: HttpClient,
    public loadingController: LoadingController,
    private toastCtrl: ToastController,
    ){}
  output = ''
  image:any=''
  imageBase64 = '';
  openCam(){

    const options: CameraOptions = {
      quality: 50,
      destinationType: this.camera.DestinationType.DATA_URL,
      encodingType: this.camera.EncodingType.JPEG,
      targetWidth: 400,
      targetHeight: 400,
      mediaType: this.camera.MediaType.PICTURE,
      correctOrientation: true
    }
    
    this.camera.getPicture(options).then((imageData) => {
     // imageData is either a base64 encoded string or a file URI
     // If it's base64 (DATA_URL):
     //alert(imageData)
     console.log(imageData)
     this.imageBase64 = 'data:image/png;base64,' + imageData
     this.image=(<any>window).Ionic.WebView.convertFileSrc(imageData);
     console.log(this.image)
    }, (err) => {
     // Handle error
     alert("error "+JSON.stringify(err))
    });

  }

  async presentLoading() {
    this.loading = await this.loadingController.create({
      message: 'Checking image...',
      spinner: 'circles'
    });
    return await this.loading.present();  
  }

  closeLoading() {
    if(this.loading){
        this.loading.dismiss();
    }
  }

  async presentToast(message) {
    const toast = await this.toastCtrl.create({
      message: message,
      duration: 3000
    });
    toast.present();
  }

  checkImage() {
    console.log(this.imageBase64)
    const data = {
      'image_data': this.imageBase64.toString().replace('data:image/png;base64,', ''),
      'res': 'json'
    }
    const form = new FormData();
    form.append('image_data', this.imageBase64.toString().replace('data:image/png;base64,', ''))
    form.append('res', 'json');

    this.presentLoading()

    this.httpClient.post('https://hearthepic.site/output', form, {headers: new HttpHeaders()
      .set('Accept', 'application/json')})
      .subscribe(
        (res) => {
          this.closeLoading();
          console.log(res)
          if (res['result']) {
            this.output = 'Output is ' + res['label']
            this.presentToast('Output computed!')
          } else {
            this.presentToast('Error computing image!')
          }
        },
        (error) => {
          this.closeLoading();
          // alert(JSON.stringify(error))
          this.presentToast('Error computing image!')
        }
      );
  }

}
