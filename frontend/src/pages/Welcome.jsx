import React from 'react';
import { Link } from 'react-router-dom';

const Welcome = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold mb-6">Welcome to Our App</h1>
      <p className="text-lg text-gray-600 mb-6">Get started by logging in or signing up.</p>
      <div className="flex space-x-4">
        <Link to="/login" className="px-6 py-3 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600">
          Login
        </Link>
        <Link to="/signin" className="px-6 py-3 bg-green-500 text-white rounded-lg shadow-md hover:bg-green-600">
          Sign Up
        </Link>
      </div>
    </div>
  );
};

export default Welcome;
