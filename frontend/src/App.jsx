// src/pages/App.jsx
import React, { useEffect, useState, useContext } from 'react';
import { fetchProtectedData } from './services/auth';
import { AuthContext } from './context/AuthContext';

const App = () => {
  const [data, setData] = useState(null);
  const { logout } = useContext(AuthContext);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetchProtectedData();
        setData(response);
      } catch (err) {
        console.error('Failed to fetch data', err);
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>Welcome to the App</h1>
      <button onClick={logout}>Logout</button>
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
};

export default App;
