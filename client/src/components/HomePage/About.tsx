import aboutcard from "../../assets/home/aboutcard.svg";
import arrow from "../../assets/home/arrowRight.svg";
import gridlines from "../../assets/grid-layer.png";
import vector from "../../assets/home/Vector.svg";
import subscribehaya from "../../assets/home/subscribehaya.png";

function About() {
  return (
    <div id="about" className="px-12 py-20">
      <div className="max-w-screen-2xl mx-auto flex justify-between gap-12 pb-20">
        <div className="flex flex-col gap-4 max-w-[505px] overflow-hidden">
          <div className="relative w-[200px] h-[75px] flex items-center justify-center">
            <img src={vector} alt="" className="absolute bottom-2 left-2" />
            <h2 className="font-semibold text-black text-2xl">About Haya</h2>
            <img
              src={vector}
              alt=""
              className="absolute top-2 right-2 rotate-180"
            />
          </div>
          <div className="flex flex-col gap-2 text-black">
            <p className="font-satoshi">
              At Haya, we're passionate about bridging the gap between companies
              and tech talents across the country.
            </p>
            <p className="font-satoshi">
              With a focus on precision matching and streamlined processes,
              we're committed to revolutionizing the way companies and
              businesses discover and connect with the right tech professionals.
              Whether you're a startup, a scale-up, or an enterprise, we're here
              to help you unlock the potential of your workforce.
            </p>
            <p className="font-satoshi">
              Our platform is designed to empower tech professionals like you to
              find meaningful opportunities that align with your skills,
              passions, and career goals. Whether you're a seasoned developer or
              a rising star in the tech world, we're here to support your
              journey.
            </p>
            <p className="font-satoshi">
              Join us on the journey to reshape the future of tech talent
              acquisition!
            </p>
          </div>
          <button className="font-satoshi text-white bg-primary self-start p-4 rounded-xl mt-4 font-medium text-sm">
            Request access to Haya
            <img src={arrow} alt="" className="inline-block ml-2" />
          </button>
        </div>

        <img
          src={aboutcard}
          alt=""
          className="w-full h-[650px] -mt-28 select-none"
        />
      </div>

      <div
        style={{
          backgroundImage: `url(${gridlines})`,
        }}
        className="bg-no-repeat bg-center max-w-screen-2xl mx-auto h-[300px] flex items-center justify-center overflow-hidden rounded-3xl bg-[#4E5B92] relative"
      >
        <img
          src={subscribehaya}
          alt=""
          className="absolute bottom-0 right-0 select-none"
        />
        <div className="flex flex-col items-center w-1/2 mx-auto">
          <h3 className="font-semibold text-[#FBF8FF] text-2xl">
            Get Exclusive Access To Haya
          </h3>
          <p className="text-[#FBF8FF] mt-2 font-satoshi font-medium">
            Submit your email address to request exclusive access to the Haya
            search engine
          </p>
          <div className="mt-6 flex justify-between gap-2 w-full">
            <input
              type="email"
              className="bg-[#FEFBFF] min-w-[70%] grow rounded-xl text-black placeholder:text-[#ABAAB4] font-satoshi text-sm font-medium p-4 outline-none"
              placeholder="Enter email address"
            />
            <button className="bg-[#06D0FF] text-[#000C39] font-satoshi font-medium text-sm p-4 rounded-xl">
              Submit email
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default About;
