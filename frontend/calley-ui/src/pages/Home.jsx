import React from "react";
import { Link } from "react-router-dom";
import animate from '../assets/animate.gif'

function Home() {
  return (
    <div className="bg-white-100 h-screen">
      <div className="bg-white   text-gray-700 py-4 px-8 flex justify-between items-center">
        <h1 className="font-bold text-3xl">Calley</h1>
        <div className="flex gap-4 text-lg justify-center items-center font-bold">
          <Link to="/login" className="hover:underline">
            Login
          </Link>
          <Link
            to="/signup"
            className="hover:underline bg-[#57cc99] p-2 rounded text-white px-4"
          >
            Signup
          </Link>
        </div>
      </div>

      <div className="flex items-center py-28 px-8">
        <div className="">
          <h2 className="text-[3rem] font-bold mb-6">
            Welcome to Calley. Your personal event program assistant
          </h2>
          <p className="text-xl mb-8">
            Easily manage your personal event program and tasks with Calley. Our
            platform is designed to help you stay organized, on track, and on
            schedule.
          </p>
          <Link to="/dashboard" className="hover:underline py-4 px-6 bg-[#57cc99] text-[#fff] font-bold">
            Get started
          </Link>
        </div>

        <div className="ml-20 ">
          <img src={animate} height={400} width={400}/>
        </div>
      </div>
    </div>
  );
}

export default Home;
