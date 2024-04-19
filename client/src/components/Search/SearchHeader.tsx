import bell from "../../assets/notification.svg";
import cancel from "../../assets/cancel.svg";
import lens from "../../assets/search-02.svg";
import user from "../../assets/user.svg";
import arrow from "../../assets/arrow-down.svg";
import { Link } from "react-router-dom";
import React, { useEffect } from "react";

function SearchHeader({
  searchText,
  setSearchText,
}: {
  searchText: string;
  setSearchText: React.Dispatch<React.SetStateAction<string>>;
}) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Enter") {
        window.location.href = `/search?q=${searchText}`;
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [searchText]);

  return (
    <div>
      <header className="flex justify-between items-center w-full gap-2">
        <Link to="/">
          <h1 className="text-primary font-bold text-lg md:text-2xl font-satoshi">
            haya.ng
          </h1>
        </Link>

        <div className="py-2 lg:py-4 px-3 lg:px-5 hidden md:flex items-center justify-between w-3/5 bg-[#F1F0FA] rounded-xl">
          <div className="flex gap-6 items-center w-full">
            <img
              src={lens}
              alt="search"
              className={`w-6 ${searchText && "hidden"}`}
            />

            <input
              type="text"
              value={searchText}
              autoFocus
              onChange={(e) => setSearchText(e.target.value)}
              placeholder="Search talents to haya"
              className="w-full bg-transparent border-0 focus:outline-none text-[#47464A] font-medium md:text-xl font-satoshi"
            />
          </div>
          <span className={`cursor-pointer ${!searchText && "hidden"}`}>
            <img src={cancel} alt="cancel" onClick={() => setSearchText("")} />
          </span>
        </div>

        <div className="flex items-center gap-4">
          <span className="bg-[#F1F0FA] p-3 rounded-xl cursor-pointer">
            <img src={bell} alt="notification" />
          </span>
          <div className="flex items-center gap-2 bg-[#F1F0FA] p-3 rounded-xl cursor-pointer">
            <img src={user} alt="user" />
            <span className="text-secondary font-medium text-sm w-[100px] truncate overflow-hidden hidden md:block font-satoshi">
              {"Bankole Davis"}
            </span>
            <img src={arrow} alt="" />
          </div>
        </div>
      </header>
      <div className="py-2 lg:py-4 px-3 lg:px-5 md:hidden my-4 flex items-center justify-between w-full bg-[#F1F0FA] rounded-xl">
        <div className="flex gap-6 items-center w-full">
          <img
            src={lens}
            alt="search"
            className={`w-6 ${searchText && "hidden"}`}
          />

          <input
            type="text"
            value={searchText}
            autoFocus
            onChange={(e) => setSearchText(e.target.value)}
            placeholder="Search talents to haya"
            className="w-full bg-transparent border-0 focus:outline-none text-[#47464A] font-medium text-xl font-satoshi"
          />
        </div>
        <span className={`cursor-pointer ${!searchText && "hidden"}`}>
          <img
            className="w-6"
            src={cancel}
            alt="cancel"
            onClick={() => setSearchText("")}
          />
        </span>
      </div>
    </div>
  );
}

export default SearchHeader;
