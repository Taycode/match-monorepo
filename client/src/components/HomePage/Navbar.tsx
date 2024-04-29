import logo from "../../assets/logo.svg";

function Navbar() {
  return (
    <div className="border-y border-[#E9E7EC] border-solid">
      <header className="flex justify-between items-center max-w-screen-2xl px-12 mx-auto bg-transparent py-8 relative">
        <div className="absolute top-0 right-0 left-0 h-full z-1 border-x border-[#E9E7EC] border-solid max-w-[1230px] mx-auto w-full"></div>
        <ul className="flex items-center gap-x-8 py-8 z-10">
          <li>
            <a
              href="/#about"
              className="font-medium text-[#1A1B21] bg-[#FBF8FF]"
            >
              About
            </a>
          </li>
          <li>
            <a
              href="/#how-it-works"
              className="font-medium text-[#1A1B21] bg-[#FBF8FF]"
            >
              How It Works
            </a>
          </li>
          <li>
            <a
              href="/#faqs"
              className="font-medium text-[#1A1B21] bg-[#FBF8FF]"
            >
              FAQs
            </a>
          </li>
        </ul>
        <a href="/" className="z-10">
          <img src={logo} alt="logo" />
        </a>
        <div className="flex items-center gap-4">
          <a href="/signin" className="z-10">
            <button className="bg-[#F1F0FA] rounded-xl py-3 font-satoshi text-sm text-primary font-medium w-[120px]">
              Login
            </button>
          </a>
          <button className="bg-primary rounded-xl z-10 py-3 font-satoshi text-sm text-white font-medium w-[120px]">
            Request Access
          </button>
        </div>
      </header>
    </div>
  );
}

export default Navbar;
