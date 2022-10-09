
export interface DataApiResponse<T> {
    data: T[]
}

export interface LoginApiResponse {
    loggedin: boolean,
    user_id: number,
    user_name: string
}

export interface RegisterApiResponse {
    register: boolean,
}