import FilterModal from "./FilterModal";
import back from "../../assets/back.svg";
import cancel from "../../assets/cancel.svg";
import deleted from "../../assets/delete.svg";
import { FilterIcon } from "../../assets/icons";
import useStore from "../../store";
import { TalentType } from "../../store/data";
import UserCard from "./UserCard";
import { useState } from "react";
import UserProfile from "./UserProfile";

function Hero({
  queryParamValue,
  talents,
  filters,
  setFilters,
}: {
  queryParamValue: string | null;
  talents: TalentType[];
  filters: { [key: string]: string };
  setFilters: React.Dispatch<React.SetStateAction<{ [key: string]: string }>>;
}) {
  const { setModal } = useStore();
  const [isUserProfileOpen, setIsUserProfileOpen] = useState(false);
  const [talendId, setTalentId] = useState<string>("");

  return (
    <div>
      <div className="flex justify-between items-center my-4 md:my-8">
        <button className="p-3 rounded-xl bg-[#F1F0FA] flex items-center gap-1 md:gap-2">
          <img src={back} alt="back" />
          <span className="text-primary text-sm">Back</span>
        </button>
        <p
          className={`text-[#77767A] hidden font-medium md:block text-base ${
            !queryParamValue && "hidden"
          }`}
        >
          Showing{" "}
          <span className="text-[#1A1B21] font-medium">
            {talents.length} {queryParamValue}{" "}
          </span>
          talent{talents.length > 1 && "s"} for haya!
        </p>

        <button
          onClick={() =>
            setModal(<FilterModal filters={filters} setFilters={setFilters} />)
          }
          className={`p-3 rounded-xl ${
            Object.values(filters).some((filter) => filter !== "")
              ? "bg-primary text-white"
              : "bg-[#F1F0FA] text-primary"
          }  flex items-center gap-2`}
        >
          <FilterIcon
            color={
              Object.values(filters).some((filter) => filter !== "")
                ? "white"
                : "#092470"
            }
          />
          <span className="text-sm">Filter</span>
        </button>
      </div>
      <p
        className={`text-[#77767A] font-medium md:hidden text-sm text-center ${
          !queryParamValue && "hidden"
        }`}
      >
        Showing{" "}
        <span className="text-[#1A1B21] font-medium">
          {talents.length} {queryParamValue}{" "}
        </span>
        talent{talents.length > 1 && "s"} for haya!
      </p>

      <div className="flex flex-wrap justify-between gap-3 items-center w-full my-4 md:my-8">
        <div className="flex items-center gap-2">
          {Object.keys(filters).map((filter: string) => (
            <div
              key={filter}
              className={`flex items-center gap-1 md:gap-2 bg-[#DDE1FF] border border-[#05164B] border-solid rounded-xl p-1.5 md:p-2 ${
                !filters[filter] && "hidden"
              } `}
            >
              <span className="text-[#05164B] text-sm">{filters[filter]}</span>
              <button
                className="bg-transparent w-4 md:w-6"
                onClick={() =>
                  setFilters({
                    ...filters,
                    [filter]: "",
                  })
                }
              >
                <img src={cancel} alt="cancel" className="w-4" />
              </button>
            </div>
          ))}
        </div>
        <button
          onClick={() =>
            setFilters({
              experience: "",
              matchScore: "",
            })
          }
          className={`bg-[#F1F0FA] rounded-xl p-1 md:p-3 flex gap-0.5 md:gap-2 text-primary font-satoshi text-sm font-medium ${
            !filters.experience && !filters.matchScore && "hidden"
          }`}
        >
          <img src={deleted} alt="deleted" className="w-4" />
          Clear all filters
        </button>
      </div>

      <div className="flex justify-between gap-4 w-full">
        <div className="flex flex-col gap-4 max-w-7xl mx-auto w-full">
          {talents.length > 0 ? (
            talents.map((talent) => (
              <UserCard
                key={talent.id}
                {...{
                  talent,
                  setIsUserProfileOpen,
                  setTalentId,
                  talents,
                  isUserProfileOpen,
                }}
              />
            ))
          ) : (
            <p className="text-center text-[#77767A] font-medium">
              No talent found
            </p>
          )}
        </div>
        <UserProfile
          {...{ isUserProfileOpen, talendId, talents, setIsUserProfileOpen }}
        />
      </div>
    </div>
  );
}

export default Hero;
