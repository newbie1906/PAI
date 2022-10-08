import { Component, OnInit, Input } from '@angular/core';
import { Message } from '../message';

@Component({
  selector: 'app-chat-message-list',
  templateUrl: './chat-message-list.component.html',
  styleUrls: ['./chat-message-list.component.scss']
})
export class ChatMessageListComponent implements OnInit {

  // Dane wejściowe komponentu - wiadomości oraz id użytkownika
  @Input() messages:Message[] = [];
  @Input() myId:number = 0;
  
  constructor() { }

  ngOnInit() {
  }

}
