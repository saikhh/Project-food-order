import React, { useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";

const Register = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const { register } = useContext(AuthContext);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    register(formData.username, formData.email, formData.password);
  }

  return ( 
    <form onSubmit={handleSubmit}>
      <input
        type="text" name="username" placeholder="Username" value={formData.username} onChange={handleChange} required />
      <input
        type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
      <input
        type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} required />
      <button type="submit">Register</button>
    </form>
  )
};


export default Register; 