import { motion } from "framer-motion";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import arrowEnter from "../../assets/arrow-back.svg";
import cancel from "../../assets/cancel.svg";
import lens from "../../assets/search-02.svg";
import logo from "../../assets/searchenginehaya.svg";
import { topLeftVariants } from "../../utils/transitions";
import useStore from "../../store";

function StepTwo({
  currentModal,
  setStep,
}: {
  currentModal: any;
  setStep: React.Dispatch<React.SetStateAction<number>>;
}) {
  const [searchText, setSearchText] = useState("");
  const [, setLoading] = useState(false);
  const navigate = useNavigate();

  const setModal = useStore((state: any) => state.setModal);

  useEffect(() => {
    const handleKeyPress = (event: any) => {
      if (event.key === "Escape") {
        setStep(1);
      } else if (event.key === "Enter") {
        if (!searchText) return;
        setLoading(true);
        setModal(<Modal />);
        setTimeout(() => {
          navigate(`/search?q=${searchText}`);
          setModal(null);
        }, 3000);
        setLoading(false);
      }
    };

    document.addEventListener("keydown", handleKeyPress);

    return () => {
      document.removeEventListener("keydown", handleKeyPress);
    };
  }, [searchText]);

  return (
    <motion.div
      variants={topLeftVariants}
      initial="hidden"
      whileInView="visible"
      className={`max-w-7xl mx-auto flex flex-col h-full p-4 md:p-8 relative ${
        currentModal && "blur-sm"
      }`}
    >
      <img src={logo} alt="logo" className="absolute bottom-0 -left-12" />
      <div className="p-4 z-10 flex items-center justify-between w-full border-0 border-b border-solid border-[#C6C5CF]">
        <div className="flex gap-6 items-center w-full">
          <img
            src={lens}
            alt="search"
            className={`w-6 md:w-12 ${searchText && "hidden"}`}
          />
          <input
            type="text"
            autoFocus
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            placeholder="Search talents to haya"
            className="w-full py-4 bg-transparent border-0 focus:outline-none placeholder:text-[#C6C5CF] text-[#525256] text-xl md:text-4xl"
          />
        </div>
        <span
          className={`p-2 rounded-xl bg-[#F1F0FA] cursor-pointer ${
            !searchText && "hidden"
          }`}
        >
          <img src={cancel} alt="cancel" onClick={() => setSearchText("")} />
        </span>
      </div>
      <p className="mt-6 z-10 text-[#77767A] font-medium text-sm md:text-xl flex items-center">
        Press
        <span className="flex gap-2 justify-center mx-2 w-[80px] md:w-[120px] py-2.5 bg-[#E2E1EC] rounded-lg font-bold text-[#45464E]">
          Enter <img src={arrowEnter} />
        </span>
        on the keyboard to search
      </p>

      <div className="z-10 absolute bottom-4 flex w-full justify-center">
        <div
          onClick={() => setStep(1)}
          className="bg-[#F1F0FA] p-2 rounded-xl flex items-center gap-4"
        >
          <span className="p-1.5 rounded-xl bg-[#C6C5CF] font-bold text-secondary text-sm">
            esc
          </span>
          <span className="text-primary font-medium text-lg">Close</span>
        </div>
      </div>
    </motion.div>
  );
}

export default StepTwo;

function Modal() {
  return (
    <div className="flex items-center flex-col justify-center relative">
      <div className="loader absolute" />
      <p className="text-[#B7C4FF] font-bold md:text-xl mt-40">
        Searching for talents
      </p>
    </div>
  );
}
