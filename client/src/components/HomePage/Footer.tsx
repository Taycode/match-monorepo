import footerhaya from "../../assets/home/footerhaya.svg";
import lnkdin from "../../assets/home/LinkedIn.svg";
import twtr from "../../assets/home/TwitterX.svg";
import igram from "../../assets/home/Instagram.svg";
import sprinkle from "../../assets/home/sprinkle.svg";

function Footer() {
  return (
    <div className="max-w-screen-2xl mx-auto pb-12 md:pb-20 px-4 md:px-8 lg:px-12">
      <div className="bg-[#F1F0FA] rounded-3xl py-4 px-4 md:px-6 lg:px-8 flex flex-col gap-16 relative overflow-hidden">
        <img
          src={sprinkle}
          alt="sprinkle"
          className="absolute -top-16 left-16"
        />
        <img
          src={sprinkle}
          alt="sprinkle"
          className="absolute -bottom-[60%] left-[50%]"
        />
        <img src={sprinkle} alt="sprinkle" className="absolute top-0 right-0" />
        <div className="flex flex-wrap md:flex-nowrap justify-center gap-4 md:gap-0 md:justify-between items-center z-10">
          <a href="/">
            <img src={footerhaya} alt="haya" />
          </a>
          <ul className="flex items-center gap-4 lg:gap-8">
            <li>
              <a
                href="/#about"
                className="font-medium text-[#1A1B21] text-sm lg:text-base"
              >
                About Haya
              </a>
            </li>
            <li>
              <a
                href="/#how-it-works"
                className="font-medium text-[#1A1B21] text-sm lg:text-base"
              >
                How Haya Works
              </a>
            </li>
            <li>
              <a
                href="/#faqs"
                className="font-medium text-[#1A1B21] text-sm lg:text-base"
              >
                FAQs
              </a>
            </li>
          </ul>
          <div className="flex items-center gap-4">
            <a href="/signin">
              <button className="bg-[#E2E1EC] rounded-xl py-3 font-satoshi text-sm text-primary font-medium w-[120px]">
                Login
              </button>
            </a>
            <button className="bg-[#1A1B21] rounded-xl py-3 font-satoshi text-sm text-white font-medium w-[120px]">
              Request Access
            </button>
          </div>
        </div>
        <div className="flex flex-col md:flex-row gap-4 justify-between items-center z-10">
          <ul className="flex items-center gap-x-8">
            <li>
              <a href="#">
                <img src={lnkdin} alt="linkedin" />
              </a>
            </li>
            <li>
              <a href="#">
                <img src={twtr} alt="twitter" />
              </a>
            </li>
            <li>
              <a href="#">
                <img src={igram} alt="instagram" />
              </a>
            </li>
          </ul>
          <p className="text-[#1A1B21] font-satoshi text-sm font-medium">
            Copyright © Haya 2024
          </p>
          <a
            href="mailto:help@hayang.com"
            target="_blank"
            className="text-[#1A1B21] font-satoshi font-medium"
          >
            support: <span className="ml-1 font-semibold">help@hayang.com</span>
          </a>
        </div>
      </div>
    </div>
  );
}

export default Footer;
