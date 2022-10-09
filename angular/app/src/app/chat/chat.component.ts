import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpService } from '../http.service';
import { User } from '../user';
import { Message } from '../message';
import { DataApiResponse } from '../api-response';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})
export class ChatComponent {

 
  // lista użytkowników
  users: User[] = [];

  // lista wiadomości z wybranym uzytkownikiem
  messagesToUser: Message[] = [];

  // wybrany uzytkownik
  selectedUser: User = {} as User;

  constructor(
    private router: Router,
    private httpService: HttpService,
  ) {
    // Sprawdzenie czy uzytkownik nie jest zalogowany, jezeli tak - przejscie do głownego panelu
    if (!httpService.isLogin) {
      this.router.navigate(['/login']);
    }
  }

  ngOnInit() {
    this.reloadUsers();
  }


  // Funkcja zwracająca nasze ID
  getMyId() {
    return this.httpService.loginUserData.user_id;
  }

  // Funkcja wysyłająca wiadomość
  sendMessage(e: string) {
    this.httpService.sendMessages(new Message(this.getMyId(),this.selectedUser.user_id,e)).subscribe({
      next: (data) => {
        console.log("ChatComponent, onSubmit:", data);
      },
      error: (error) => {
      }
    });
  }

  // Funkcja przeładowująca listę użytkowników
  reloadUsers() {
    this.httpService.getUsers().subscribe({
      next: (data) => {
        if (data.hasOwnProperty("data")) {
          let responseData = data as DataApiResponse<User>;
          if (Array.isArray(responseData.data)) {
            this.users = responseData.data;
          }
        }
      },
      error: (error) => {
      }
    });
  }

  // funkcja wywoływana gdy zostanie wybrany użytkownik na liście użytkowników
  userSelected(user: User) {
    this.selectedUser = user;
    console.log("Selected user", this.selectedUser)
    this.getMessagesWithSelectedUser();
  }

  // Funkcja pobierające listę wiadomości z danym użytkownikiem
  getMessagesWithSelectedUser() {
    // uzupełnij funkcję na podstawie funkcji realoadUsers
    this.httpService.getMessages(this.selectedUser.user_id).subscribe({
      next: (data) => {
        if (data.hasOwnProperty("data")) {
          let responseData = data as DataApiResponse<Message>;
          if (Array.isArray(responseData.data)) {
            this.messagesToUser = responseData.data;
          }
        }
      },
      error: (error) => {
      }
    });
  }

}
