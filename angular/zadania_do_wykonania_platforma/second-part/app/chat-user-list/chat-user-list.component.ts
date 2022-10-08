import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { User } from '../user';

@Component({
  selector: 'app-chat-user-list',
  templateUrl: './chat-user-list.component.html',
  styleUrls: ['./chat-user-list.component.scss']
})
export class ChatUserListComponent implements OnInit {

  // Dane wejściowe komponentu - lista uzytkownikow
  @Input() users: User[] = [];

  // Dane wyjsciowe z komponentu - zdarzenie wywoływane po naciśnieciu uzytkownika
  @Output() userClicked: EventEmitter<User> = new EventEmitter();
  
  constructor() { }

  ngOnInit() {

  }
}
