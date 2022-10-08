import { Injectable, EventEmitter } from '@angular/core';
import { Message } from './message';

@Injectable({
  providedIn: 'root'
})
export class MessageWSService {

  ws: any;

  // Event służący do informowania o nadejściu wiadomości
  onMessage: EventEmitter<Message> = new EventEmitter();

  // Event służący do informowania o połączeniu się nowego użytkownika
  onAnotherUserConneted: EventEmitter<boolean> = new EventEmitter();

  // Event służący do informowania o zerwaniu połączenia
  onClose: EventEmitter<boolean> = new EventEmitter();

  // Event służący do informowania o połączeniu
  onOpen: EventEmitter<boolean> = new EventEmitter();

  isOpen: boolean = false;

  constructor() {

  }

  open() {

    const self = this;

    this.ws = new WebSocket(`ws://${location.host}/stream/`);

    this.ws.onerror = function () {
      console.log('WebSocket error');
    };

    this.ws.onopen = function () {
      self.isOpen = true;
      self.onOpen.emit(true);
      console.log('WebSocket connection established');
    };

    this.ws.onclose = function () {
      self.onClose.emit(true);
      self.isOpen = false;
      console.log('WebSocket connection closed');
    };

    this.ws.onmessage = function (msg) {
      const mes = JSON.parse(msg.data);
      if (mes["status"] == 1) {
        self.onMessage.emit(mes["data"] as Message);
      }
      if (mes["status"] == 2) {
        self.onAnotherUserConneted.emit(true);
      }

      console.log('WebSocket message', msg.data);
    };
  }
}
