import Logo from "../Logo";
import arrow from "../../assets/arrow-down.svg";
import bell from "../../assets/notification.svg";
import global from "../../assets/global.svg";
import help from "../../assets/messages.svg";
import instagram from "../../assets/Instagram.svg";
import lens from "../../assets/search-02.svg";
import search from "../../assets/searching.svg";
import twitter from "../../assets/twitter.svg";
import user from "../../assets/user.svg";

import { useEffect } from "react";

function StepOne({
  setStep,
}: {
  setStep: React.Dispatch<React.SetStateAction<number>>;
}) {
  useEffect(() => {
    const handleKeyPress = (event: any) => {
      if (event.key === "Enter") {
        setStep(2);
      }
    };

    document.addEventListener("keydown", handleKeyPress);

    return () => {
      document.removeEventListener("keydown", handleKeyPress);
    };
  }, []);

  return (
    <div className="max-w-screen-2xl mx-auto flex flex-col h-full p-4 md:p-8 relative">
      <div className="self-end flex items-center gap-4 mb-12 md:mb-0">
        <span className="bg-[#F1F0FA] p-3 rounded-xl cursor-pointer">
          <img src={bell} alt="notification" />
        </span>
        <div className="flex items-center gap-2 bg-[#F1F0FA] p-3 rounded-xl cursor-pointer">
          <img src={user} alt="user" />
          <span className="text-secondary font-medium text-sm">
            {"Bankole Davis"}
          </span>
          <img src={arrow} alt="" />
        </div>
      </div>

      <div className="max-w-5xl w-full mx-auto flex flex-col items-center gap-8">
        <Logo />
        <a href="/">
          <h2 className="text-primary font-black text-6xl">haya.ng</h2>
        </a>
        <p className="font-medium text-[#05164B]">
          Your preferred tech talent search engine
        </p>
        <div
          onClick={() => setStep(2)}
          className="flex justify-center items-center w-full py-8 gap-4 cursor-pointer bg-[#F1F0FA] rounded-xl"
        >
          <img src={lens} alt="search" />
          <img src={search} alt="search" />
          <p className="font-medium text-[#ACAAAE]">Search talents to haya</p>
        </div>
      </div>

      <div className="flex flex-col md:flex-row w-full justify-between items-center gap-4 absolute bottom-0 right-0 left-0 p-4 md:p-8">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 bg-[#F1F0FA] p-2.5 rounded-xl">
            <img src={twitter} alt="twitter" />
            <h6 className="font-medium text-primary">@hayang</h6>
          </div>
          <div className="flex items-center gap-2 bg-[#F1F0FA] p-2.5 rounded-xl">
            <img src={instagram} alt="instagram" />
            <h6 className="font-medium text-primary">@hayang</h6>
          </div>
          <div className="flex items-center gap-2 bg-[#F1F0FA] p-2.5 rounded-xl">
            <img src={global} alt="instagram" />
            <h6 className="font-medium text-primary">haya.ng</h6>
          </div>
        </div>
        <div className="flex items-center gap-2 bg-[#F1F0FA] p-2.5 rounded-xl">
          <img src={help} alt="instagram" />
          <h6 className="font-medium text-primary">Help</h6>
        </div>
      </div>
    </div>
  );
}

export default StepOne;
