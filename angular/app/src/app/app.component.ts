import { Component } from '@angular/core';
import { HttpService } from './http.service';
import { Router } from '@angular/router';
import { LoginApiResponse } from './api-response';
import { User } from './user';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  constructor(
    public httpService: HttpService,
    private router: Router) {
  }

  logout() {
    this.httpService.logout().subscribe(
      data => {
        if (data.hasOwnProperty("loggedin")) {
          let responseData = data as LoginApiResponse;
          if (responseData.loggedin === false) {
            this.httpService.isLogin = false;
            this.httpService.user = {} as User;
            this.router.navigate(['/login']);
          }
        }
      });
  }
}
