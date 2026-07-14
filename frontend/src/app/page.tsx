"use client";
import Navbar from "@/components/landing/Navbar";
import Hero from "@/components/landing/Hero";
import Features from "@/components/landing/Features";
import Screenshot from "@/components/landing/Screenshot";
import Footer from "@/components/landing/Footer";

import {useEffect} from "react";
import {getCurrentUser} from "@/lib/auth";
import {useRouter} from "next/navigation";



export default function LandingPage() {
  const router = useRouter();

  useEffect(()=> {
    async function checkAuth(){
      const token = localStorage.getItem("token");

      if(!token) return;

      const user = await getCurrentUser();
      if (!user) {
        localStorage.removeItem("token");
        return;
      }
      if (user.is_guest){
        localStorage.removeItem("token");
        return;
      }
      router.replace("/app");
    
    }
    checkAuth();
  }, []);


  return (
    <main className="min-h-screen bg-zinc-950 text-white">
      <Navbar />
      <Hero />
      <Features />
      <Footer />
    </main>
  );
}