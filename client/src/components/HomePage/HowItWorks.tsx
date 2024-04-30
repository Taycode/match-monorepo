import home from "../../assets/home/home.svg";
import search from "../../assets/home/search.svg";
import searchengine from "../../assets/home/searchengine.svg";
import signin from "../../assets/home/signin.svg";
import vector from "../../assets/home/Vector.svg";

function HowItWorks() {
  return (
    <div
      id="how-it-works"
      className="px-4 md:px-6 lg:px-12 py-2 md:py-20 max-w-screen-2xl mx-auto"
    >
      <div className="relative w-[270px] h-[75px] flex items-center justify-center">
        <img src={vector} alt="" className="absolute bottom-2 left-2" />
        <h2 className="font-semibold text-black text-2xl">How Haya Works</h2>
        <img
          src={vector}
          alt=""
          className="absolute top-2 right-2 rotate-180"
        />
      </div>

      <div className="mt-6 flex flex-col gap-4 w-full">
        <div className="bg-[#F1F0FA] rounded-2xl relative flex flex-col lg:flex-row gap-4 lg:items-center justify-between overflow-hidden lg:h-[438px] px-8 py-4">
          <h4 className="absolute -top-12 lg:top-[8%] -left-4 text-[12rem] text-[#E2E1EC] font-bold">
            1
          </h4>
          <div className="max-w-[500px] z-10">
            <h3 className="text-[#1A1B21] font-bold text-xl font-satoshi">
              Request Access
            </h3>
            <p className="mt-1 text-[#1A1B21] font-satoshi">
              You'll receive an email containing your login details. Proceed to
              use this login details to sign into the search engine.
            </p>
            <button className="font-satoshi text-white bg-primary self-start p-4 rounded-xl mt-8 font-medium text-sm">
              Request access
            </button>
          </div>
          <img src={home} alt="" className="z-10" />
        </div>
        <div className="bg-[#F1F0FA] rounded-2xl relative flex flex-col lg:flex-row gap-4 lg:items-center justify-between overflow-hidden lg:h-[438px] px-8 py-4">
          <h4 className="absolute -top-12 lg:top-[8%] -left-4 text-[12rem] text-[#E2E1EC] font-bold">
            2
          </h4>
          <div className="max-w-[500px] z-10">
            <h3 className="text-[#1A1B21] font-bold text-xl font-satoshi">
              Sign In to Search Engine
            </h3>
            <p className="mt-1 text-[#1A1B21] font-satoshi">
              You'll receive an email containing your login details. Proceed to
              use this login details to sign into the search engine.
            </p>
            <button className="font-satoshi text-white bg-primary self-start p-4 rounded-xl mt-8 font-medium text-sm">
              Request access
            </button>
          </div>
          <img src={signin} alt="" className="z-10" />
        </div>
        <div className="bg-[#F1F0FA] rounded-2xl relative flex flex-col lg:flex-row gap-4 lg:items-center justify-between overflow-hidden lg:h-[438px] px-8 py-4">
          <h4 className="absolute -top-12 lg:top-[8%] -left-4 text-[12rem] text-[#E2E1EC] font-bold">
            3
          </h4>
          <div className="max-w-[500px] z-10">
            <h3 className="text-[#1A1B21] font-bold text-xl font-satoshi">
              Search for talents
            </h3>
            <p className="mt-1 text-[#1A1B21] font-satoshi">
              Use the search engine to search for talents that fit the role
              you're looking to hire for.
            </p>
            <button className="font-satoshi text-white bg-primary self-start p-4 rounded-xl mt-8 font-medium text-sm">
              Request access
            </button>
          </div>
          <img src={searchengine} alt="" className="h-[90%] z-10" />
        </div>
        <div className="bg-[#F1F0FA] rounded-2xl relative flex flex-col lg:flex-row gap-4 lg:items-center justify-between overflow-hidden lg:h-[438px] px-8 py-4">
          <h4 className="absolute -top-12 lg:top-[8%] -left-4 text-[12rem] text-[#E2E1EC] font-bold">
            4
          </h4>
          <div className="max-w-[500px] z-10">
            <h3 className="text-[#1A1B21] font-bold text-xl font-satoshi">
              Browse through talents for Haya!
            </h3>
            <p className="mt-1 text-[#1A1B21] font-satoshi">
              Browse through a library of tech talents that match the role you
              wish to hire for.
            </p>
            <button className="font-satoshi text-white bg-primary self-start p-4 rounded-xl mt-8 font-medium text-sm">
              Request access
            </button>
          </div>
          <img src={search} alt="" className="h-[90%] z-10" />
        </div>
      </div>
    </div>
  );
}

export default HowItWorks;
