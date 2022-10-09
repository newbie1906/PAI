import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { LoginApiResponse } from '../api-response';
import { HttpService } from '../http.service';
import { MessageWSService } from '../message-ws.service';
import { User } from '../user';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

    // obiekt formularza
    loginForm: FormGroup = {} as FormGroup;
    // zapisanie informacji o tym, że dane zostały wysłane do serwera i jesteśmy w trakcie oczekiwania na dane
    loading = false;
    // zapisanie informacji o tym, że użytkownik nacisnął przycisk akceptujący formularz
    submitted = false;
    // lista błędów otrzymanych z serwera
    serverErrors: String[] = [];

  constructor(
    private formBuilder: FormBuilder,
    private router: Router,
    private httpService: HttpService,
    private MessageWSService: MessageWSService
  ) {
    // Sprawdzenie czy uzytkownik nie jest zalogowany, jezeli tak - przejscie do głownego panelu
    if (httpService.isLogin) {
      this.router.navigate(['/']);
    }
  }

  ngOnInit() {
    // Tworzenie grupy pól formularza
    this.loginForm = this.formBuilder.group({
      user_name: ['', [Validators.required, Validators.minLength(3)]],
      user_password: ['', [Validators.required, Validators.minLength(3)]]
    });
  }

  // Getter zwracający pola formularza
  get formControls() {
    return this.loginForm.controls;
  }

  onSubmit() {
    this.submitted = true;
    this.serverErrors = [];

    // Sprawdzenie poprawności danych w formularzu
    if (this.loginForm.invalid) {
      return;
    }

    this.loading = true;

    // Stworzenie obiektu uzytkownika z danych formularza i przesłanie ich do serwera
    this.httpService.login(new User(0, this.loginForm.controls["user_name"].value, this.loginForm.controls["user_password"].value))
      // Subskrybcja do strumienia danych zwrotnych z zapytania http
      .subscribe({
        next: (data) => {
          if (data.hasOwnProperty("loggedin")) {
            let responseData = data as LoginApiResponse;
            if (responseData.loggedin === true) {
              this.MessageWSService.open();
              // Zapisanie informacji o tym, że udało się zalogować użytkownika oraz jego dane
              this.httpService.isLogin = true;
              this.httpService.user = new User(responseData.user_id, responseData.user_name, "");
              console.log(responseData.user_id, responseData.user_name)
              this.router.navigate(['/']);
            } else {
              this.loading = false;
              // dodanie błędów do listy jeżeli nie udało się zarejestrować użytkownika
              this.serverErrors.push(JSON.stringify(data));
              console.log("LoginComponent, onSubmit:", data);
            }
          } else {
            this.loading = false;
            // dodanie błędów do listy jeżeli nie udało się zarejestrować użytkownika
            this.serverErrors.push(JSON.stringify(data));
            console.log("LoginComponent, onSubmit:", data);
          }

        },
        error: (error) => {
          this.loading = false;
        }});

  }

}
