export class Message {
    message_from_user_id: number;
    message_to_user_id: number;
    message_text: string;


    constructor( message_from_user_id: number, message_to_user_id: number, message_text: string) {
        this.message_from_user_id = message_from_user_id
        this.message_to_user_id = message_to_user_id
        this.message_text = message_text
    }
}