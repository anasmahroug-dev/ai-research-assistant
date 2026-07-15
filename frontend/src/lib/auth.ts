import { API_URL } from "./api";


export async function register(
    username: string,
    email: string,
    password: string
){
    const response = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username,
            email,
            password,   
        }), 
    });

    const data = await response.json();

    if (!response.ok){
        throw new Error(data.detail || data.error || "Registration failed");
    }

    return data;


}

export async function login(
    email: string,
    password: string
) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email,
            password,            
        }),
    });

    const data = await response.json();

    if (!response.ok){
        throw new Error(data.detail || data.error || "Login failed");
    }

    localStorage.setItem("token", data.access_token);

    return data;
}

export async function getCurrentUser(){
    const token = localStorage.getItem("token");

    if (!token){
        return null;
    }

    const response = await fetch(`${API_URL}/auth/me`,{
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    if (!response.ok){
        localStorage.removeItem("token");
        return null;
    }

    return await response.json();
}

export function logout(){
    localStorage.removeItem("token");
}

export async function guestLogin(){
    const response = await fetch(`${API_URL}/auth/guest`,{
        method: "POST",
    });

    const data = await response.json();

    if (!response.ok){
        throw new Error(data.detail || "Guest login failed");
    }

    localStorage.setItem("token", data.access_token);

    return data;
}