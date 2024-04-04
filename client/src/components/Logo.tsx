import { useEffect, useState } from "react";
import { VectorOne, VectorTwo, VectorThree } from "../assets/icons";

function Logo() {
  const [colors, setColors] = useState({
    fillOne: "#112975",
    fillTwo: "#112975",
    fillThree: "#112975",
    bg: "#B7C4FF",
  });

  const [swapPositions, setSwapPositions] = useState(false);
  const [rotateTwo, setRotateTwo] = useState(false);

  useEffect(() => {
    const bgInterval = setInterval(() => {
      setColors((prevColors) => ({
        ...prevColors,
        bg: prevColors.bg === "#B7C4FF" ? "#E3BBD9" : "#B7C4FF",
      }));
    }, 5000);

    const colorInterval = setInterval(() => {
      setColors((prevColors) => ({
        ...prevColors,
        fillOne: prevColors.fillOne === "#112975" ? "#43273E" : "#112975",
        fillTwo: prevColors.fillTwo === "#112975" ? "#43273E" : "#112975",
        fillThree: prevColors.fillThree === "#112975" ? "#43273E" : "#112975",
      }));
    }, 5000);

    const swapInterval = setInterval(() => {
      setSwapPositions(true);
      setTimeout(() => {
        setSwapPositions(false);
      }, 3000);
    }, 8000);

    const rotateTwo = setInterval(() => {
      setRotateTwo(true);

      setTimeout(() => {
        setSwapPositions(false);
        setRotateTwo(false);
      }, 2000);
    }, 4000);

    return () => {
      clearInterval(bgInterval);
      clearInterval(colorInterval);
      clearInterval(swapInterval);
      clearInterval(rotateTwo);
    };
  }, []);

  return (
    <div
      style={{
        backgroundColor: colors.bg,
        transition: "background-color 1s ease-in-out",
      }}
      className="-rotate-[8deg] p-2 rounded-xl w-[250px] flex gap-2"
    >
      <VectorOne fill={colors.fillOne} />
      <VectorTwo
        fill={colors.fillTwo}
        style={{
          transform: swapPositions
            ? `translateX(55px) rotate(120deg)`
            : rotateTwo
            ? `rotate(120deg)`
            : "none",
          transition: rotateTwo
            ? "transform 2s ease-in-out"
            : "transform 2s ease-in-out",
        }}
      />
      <VectorThree
        fill={colors.fillThree}
        style={{
          transform: swapPositions ? "translateX(-55px)" : "none",
          transition: "transform 2s ease-in-out",
        }}
      />
    </div>
  );
}

export default Logo;
