import { useEffect, useState } from "react";
import useStore from "../store";

import ModalLayout from "../components/ModalLayout";
import gridlayer from "../assets/grid-layer.png";
import StepOne from "../components/SearchEngine/StepOne";
import StepTwo from "../components/SearchEngine/StepTwo";

function SearchEngine() {
  const currentModal = useStore((state: any) => state.currentModal);
  const [step, setStep] = useState(1);
  useEffect(() => {
    if (currentModal != null) document.body.style.overflow = "hidden";
    else document.body.style.overflow = "";
  }, [currentModal]);
  return (
    <div
      style={{
        backgroundImage: `url(${gridlayer})`,
      }}
      className="w-screen h-screen bg-[#FBF8FF] bg-no-repeat bg-cover overflow-y-auto bg-center"
    >
      {currentModal && <ModalLayout />}
      {
        {
          1: <StepOne setStep={setStep} />,
          2: <StepTwo currentModal={currentModal} setStep={setStep} />,
        }[step]
      }
    </div>
  );
}

export default SearchEngine;
