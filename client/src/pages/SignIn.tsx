import { useState } from "react";
import backend from "../assets/backend.svg";
import design from "../assets/design.svg";
import frontend from "../assets/frontend.svg";
import gridlines from "../assets/grid-layer.png";
import google from "../assets/Google.svg";
import mobile from "../assets/mobile.svg";
import { EyeIcon, EyeSlashIcon, LockIcon, UserIcon } from "../assets/icons";

function SignIn() {
  const [showPassword, setShowPassword] = useState(false);
  const [formDetails, setFormDetails] = useState({
    email: "",
    password: "",
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormDetails({
      ...formDetails,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div
      style={{ backgroundImage: `url(${gridlines})` }}
      className="w-screen h-screen flex justify-center items-center bg-[#E2E1EC] bg-cover bg-no-repeat bg-center p-4"
    >
      <a
        href="/"
        className="absolute text-center top-6 md:left-20 mb-4 md:mb-0"
      >
        <h2 className="text-primary font-black text-xl md:text-2xl lg:text-4xl font-satoshi">
          haya.ng
        </h2>
      </a>
      <div className="max-w-screen-xl w-full flex justify-center relative">
        <img
          src={frontend}
          alt="frontend"
          className="hidden md:block absolute -bottom-16 lg:bottom-12 right-0 lg:right-48"
        />
        <img
          src={backend}
          alt="backend"
          className="hidden md:block absolute top-20 left-0 lg:left-32"
        />
        <img
          src={design}
          alt="design"
          className="hidden md:block absolute bottom-12 left-4"
        />
        <img
          src={mobile}
          alt="mobile"
          className="hidden md:block absolute -top-16 lg:top-3 right-0 lg:right-24"
        />
        <div className="bg-[#FBF8FF] rounded-3xl max-w-md w-full p-4 md:p-6 flex flex-col">
          <h4 className="text-center font-medium text-lg md:text-xl text-[#1A1B21]">
            Login
          </h4>
          <form className="flex flex-col gap-2 my-4 md:my-8 w-full">
            <div className="flex items-center gap-3 rounded-xl bg-[#F1F0FA] pl-3">
              <UserIcon
                fill={formDetails.email !== "" ? "#092470" : "#ACAAAE"}
              />
              <input
                type="email"
                name="email"
                onChange={handleInputChange}
                placeholder="email address"
                className="py-3 outline-none bg-transparent placeholder:text-[#ACAAAE] font-satoshi font-medium text-[#1A1B21] text-sm w-full"
              />
            </div>

            <div className="flex items-center gap-3 rounded-xl bg-[#F1F0FA] pl-3">
              <LockIcon
                fill={formDetails.password !== "" ? "#092470" : "#ACAAAE"}
              />
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                onChange={handleInputChange}
                placeholder="password"
                className="py-3 outline-none bg-transparent placeholder:text-[#ACAAAE] font-satoshi font-medium text-[#1A1B21] text-sm w-full"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="focus:outline-none h-10 text-white"
              >
                {showPassword ? <EyeSlashIcon /> : <EyeIcon className="w-5" />}
              </button>
            </div>
            <a
              href="#"
              className="text-primary text-sm font-medium font-satoshi my-2"
            >
              Reset password
            </a>
            <button className="bg-primary py-3 rounded-xl text-white font-satoshi font-medium">
              Login
            </button>
            <p className="text-center text-[#ACAAAE] text-xs font-medium mt-4 mb-2">
              Third-party login
            </p>
            <button className="bg-[#F1F0FA] flex items-center justify-center gap-3 py-3 rounded-xl text-primary font-satoshi font-medium">
              <img src={google} alt="google" />
              Login with Google
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default SignIn;
