import React, { useState } from "react";
import { TextField, InputAdornment, IconButton } from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import LockIcon from '@mui/icons-material/Lock';
import EmailIcon from '@mui/icons-material/Email';
import PortraitIcon from '@mui/icons-material/Portrait';
import { useFormik } from "formik";
import * as Yup from "yup";
import SubmitForm from "./SubmitForm";
import '../styles/register.css'

const Signin = () => {
  const [isSubmitSuccess, setIsSubmitSuccess] = useState(false);

  const formik = useFormik({
    initialValues: {
      username: "",
      password: "",
    },
    validationSchema: Yup.object({
      username: Yup.string()
        .required("Username is required!")
        .min(2, "Minimum 2 characters")
        .max(20, "Maximum 20 cheracters"),
      password: Yup.string()
        .min(8).required("Password is required!")
        .matches(
            "^(?=.*[A-Za-z])(?=.*d)(?=.*[@$!%*#?&])[A-Za-zd@$!%*#?&]{8,}$",
            "Must Contain 8 Characters, One Uppercase, One Lowercase, One Number and one special case Character"
          ),
      confirm_pass: Yup.string()
        .required("Confirm password, please!")
        .oneOf([Yup.ref("password"), null], "Passwords must match"),
      email: Yup.string()
        .required("Email is required!")
        .email("Invalid email address"),
      first_name: Yup.string(),
      last_name: Yup.string(),
    }),

    onSubmit: (values) => {
      console.log(values);
      setIsSubmitSuccess(true)
    },
  });

  return (
    <div className="register-container">
      <div className={!isSubmitSuccess ? "register register_wrapper" : "signin signin_success"}>
        {isSubmitSuccess ? (
          <SubmitForm />
        ) : (
          <form className="register-form" onSubmit={formik.handleSubmit}>
            <h2>Welcome to Innotter!</h2>
            <TextField
              name="username"
              type="text"
              placeholder="Username"
              className="input-mui"
              InputProps={{
                startAdornment: (
                  <InputAdornment>
                    <IconButton>
                      <PersonIcon />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.username}
            />

            {formik.touched.username && formik.errors.username ? (
              <div className="error_msg">{formik.errors.username}</div>
            ) : null}

            <TextField
              name="password"
              type="password"
              placeholder="Password"
              className="input-mui"
              InputProps={{
                startAdornment: (
                  <InputAdornment>
                    <IconButton>
                      <LockIcon />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.password}
            />
            {formik.touched.password && formik.errors.password ? (
              <div className="error_msg">{formik.errors.password}</div>
            ) : null}


            <TextField
              name="confirm_pass"
              type="password"
              placeholder="Confirm password"
              className="input-mui"
              InputProps={{
                startAdornment: (
                  <InputAdornment>
                    <IconButton>
                      <LockIcon />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.confirm_pass}
            />
            {formik.touched.confirm_pass && formik.errors.confirm_pass ? (
              <div className="error_msg">{formik.errors.confirm_pass}</div>
            ) : null}


            <TextField
              name="email"
              placeholder="Email"
              className="input-mui"
              InputProps={{
                startAdornment: (
                  <InputAdornment>
                    <IconButton>
                      <EmailIcon />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.email}
            />
            {formik.touched.email && formik.errors.email ? (
              <div className="error_msg">{formik.errors.email}</div>
            ) : null}


            <TextField
              name="first_name"
              placeholder="First name"
              className="input-mui"
              InputProps={{
                startAdornment: (
                  <InputAdornment>
                    <IconButton>
                      <PortraitIcon />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.first_name}
            />


            <TextField
              name="last_name"
              placeholder="Last name"
              className="input-mui"
              InputProps={{
                startAdornment: (
                  <InputAdornment>
                    <IconButton>
                      <PortraitIcon />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.last_name}
            />

            <button className="button-sign-in" type="submit">Register</button>
            <h3 className="question"> Already a member? <span className="signup">Sign in</span></h3>
          </form>
        )}
      </div>
    </div>
  );
};


export default Signin