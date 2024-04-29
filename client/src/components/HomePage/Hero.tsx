import ellipse from "../../assets/home/ellipse.svg";
import gridlines from "../../assets/grid-layer.png";
import rqA from "../../assets/home/rqA.svg";
import heroone from "../../assets/home/hero1.png";
import herotwo from "../../assets/home/hero2.png";
import herothree from "../../assets/home/hero3.png";
import herofour from "../../assets/home/hero4.png";
import herofive from "../../assets/home/hero5.png";
import herosix from "../../assets/home/hero6.png";

// Swiper
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import "swiper/css/effect-coverflow";
import "swiper/css/pagination";

// import required modules
import { EffectCoverflow, Pagination } from "swiper/modules";

function Hero() {
  return (
    <div
      style={{
        backgroundImage: `url(${gridlines})`,
      }}
      className="bg-no-repeat bg-cover bg-center pb-20"
    >
      <div className="max-w-screen-2xl px-12 mx-auto w-full pb-20">
        <h2 className="text-[#1A1B21] font-bold text-7xl py-3">
          Meet Your Tech Talent Match
        </h2>
        <div className="flex justify-between w-full items-center">
          <p className="font-satoshi text-lg text-gray max-w-[400px]">
            Explore our curated pool of top-tier tech talent meticulously
            selected to align with your company's unique needs.
          </p>
          <p className="font-satoshi text-lg text-gray max-w-[400px]">
            From seasoned developers to innovative designers, finding your
            perfect match has never been simpler.
          </p>
        </div>
        <button className="flex items-center pl-5 py-2 pr-2 rounded-full mx-auto gap-4 bg-primary text-white font-satoshi font-medium my-4">
          Request Access
          <img src={rqA} alt="Request Access" />
        </button>
      </div>
      <div className="max-w-screen-2xl w-full mx-auto relative overflow-hidden select-none">
        <img
          src={ellipse}
          alt=""
          className="absolute -top-[45%] left-0 right-0 z-10"
        />
        <Swiper
          effect={"coverflow"}
          grabCursor={true}
          // centeredSlides={true}
          slidesPerView={4}
          coverflowEffect={{
            rotate: 40,
            stretch: 0,
            depth: 100,
            modifier: 1,
            slideShadows: true,
          }}
          pagination={true}
          modules={[EffectCoverflow, Pagination]}
          className="h-[320px] bg-[#FBF8FF] w-full"
        >
          <SwiperSlide>
            <img src={heroone} alt="" className="w-full h-full" />
          </SwiperSlide>
          <SwiperSlide>
            <img src={herotwo} alt="" className="w-full h-full" />
          </SwiperSlide>
          <SwiperSlide>
            <img src={herothree} alt="" className="w-full h-full" />
          </SwiperSlide>
          <SwiperSlide>
            <img src={herofour} alt="" className="w-full h-full" />
          </SwiperSlide>
          <SwiperSlide>
            <img src={herofive} alt="" className="w-full h-full" />
          </SwiperSlide>
          <SwiperSlide>
            <img src={herosix} alt="" className="w-full h-full" />
          </SwiperSlide>
        </Swiper>
        <img
          src={ellipse}
          alt=""
          className="absolute -bottom-[45%] left-0 right-0 z-10"
        />
      </div>
    </div>
  );
}

export default Hero;
