import { useState } from "react";
import cancel from "../../assets/cancel.svg";
import reset from "../../assets/refresh-2.svg";
import tick from "../../assets/tick-02.svg";
import useStore from "../../store";

function FilterModal({
  filters,
  setFilters,
}: {
  filters: any;
  setFilters: any;
}) {
  const { setModal } = useStore();
  const [newFilters, setNewFilters] = useState({
    experience: filters.experience,
    matchScore: filters.matchScore,
  });

  const handleApplyFilters = () => {
    setFilters(newFilters);
    setModal(null);
  };

  const handleFilterChange = (category: string, value: string) => {
    setNewFilters(() => ({
      ...newFilters,
      [category]: value,
    }));
  };

  const handleReset = () => {
    setNewFilters({
      experience: "",
      matchScore: "",
    });
    setModal(null);
  };

  return (
    <div
      onClick={(e) => e.stopPropagation()}
      className="z-[200] bg-white rounded-3xl max-w-lg max-h-full no-scrollbar overflow-y-auto w-full flex flex-col p-4 md:p-6"
    >
      <div className="flex justify-between items-center">
        <h2 className="font-medium md:font-semibold md:text-xl">
          Filter Talents
        </h2>
        <span
          onClick={() => setModal(null)}
          className="bg-[#F1F0FA] p-1 rounded-xl cursor-pointer"
        >
          <img src={cancel} alt="back" />
        </span>
      </div>
      <p className="text-[#76767F] text-xs md:text-sm font-medium mt-1 md:mt-3 mb-2 md:mb-4 font-satoshi">
        Filter talents by skill, experience and match score to find the ideal
        talent(s) to haya.
      </p>
      <div>
        <h3 className="mb-1 md:mb-2 text-[#1a1b21] text-sm md:text-base font-medium">
          Experience level
        </h3>
        <ul className="ml-2 flex flex-col gap-1 md:gap-2">
          <li className="flex items-center justify-between w-full">
            <div className="flex gap-2 items-center">
              <input
                type="checkbox"
                className="checked:accent-primary"
                checked={newFilters.experience === "Entry-level"}
                onChange={() => handleFilterChange("experience", "Entry-level")}
              />
              <label className="font-satoshi text-sm md:text-base">
                Entry level
              </label>
            </div>
            <p className="text-[#919094] font-satoshi text-sm md:text-base font-medium">
              {"< 1yr exp"}
            </p>
          </li>
          <li className="flex items-center justify-between w-full">
            <div className="flex gap-2 items-center">
              <input
                type="checkbox"
                className="checked:accent-primary"
                checked={newFilters.experience === "Junior-level"}
                onChange={() =>
                  handleFilterChange("experience", "Junior-level")
                }
              />
              <label className="font-satoshi text-sm md:text-base">
                Junior level
              </label>
            </div>
            <p className="text-[#919094] font-satoshi text-sm md:text-base font-medium">
              {"1yr - 2yrs exp"}
            </p>
          </li>
          <li className="flex items-center justify-between w-full">
            <div className="flex gap-2 items-center">
              <input
                type="checkbox"
                className="checked:accent-primary"
                checked={newFilters.experience === "Mid-level"}
                onChange={() => handleFilterChange("experience", "Mid-level")}
              />
              <label className="font-satoshi text-sm md:text-base">
                Mid level
              </label>
            </div>
            <p className="text-[#919094] font-satoshi text-sm md:text-base font-medium">
              {"2yrs - 4yrs exp"}
            </p>
          </li>
          <li className="flex items-center justify-between w-full">
            <div className="flex gap-2 items-center">
              <input
                type="checkbox"
                className="checked:accent-primary"
                checked={newFilters.experience === "Senior-level"}
                onChange={() =>
                  handleFilterChange("experience", "Senior-level")
                }
              />
              <label className="font-satoshi text-sm md:text-base">
                Senior level
              </label>
            </div>
            <p className="text-[#919094] font-satoshi text-sm md:text-base font-medium">
              {"4+ yrs exp"}
            </p>
          </li>
        </ul>
      </div>
      <div className="mt-2 md:mt-4">
        <h3 className="mb-1 md:mb-2 text-[#1a1b21] text-sm md:text-base font-medium">
          Match score
        </h3>
        <ul className="ml-2 flex flex-col gap-2">
          <li className="flex items-center justify-between w-full">
            <div className="flex gap-2 items-center">
              <input
                type="checkbox"
                className="checked:accent-primary"
                checked={newFilters.matchScore === "< 5.0"}
                onChange={() => handleFilterChange("matchScore", "< 5.0")}
              />
              <label className="font-satoshi text-sm md:text-base">
                {"< 5.0"}
              </label>
            </div>
          </li>
          <li className="flex items-center justify-between w-full">
            <div className="flex gap-2 items-center">
              <input
                type="checkbox"
                className="checked:accent-primary"
                checked={newFilters.matchScore === "5.0-7.5"}
                onChange={() => handleFilterChange("matchScore", "5.0-7.5")}
              />
              <label className="font-satoshi text-sm md:text-base">
                {"5.0 - 7.5"}
              </label>
            </div>
          </li>
          <li className="flex items-center justify-between w-full">
            <div className="flex gap-2 items-center">
              <input
                type="checkbox"
                className="checked:accent-primary"
                checked={newFilters.matchScore === "7.5-9.0"}
                onChange={() => handleFilterChange("matchScore", "7.5-9.0")}
              />
              <label className="font-satoshi text-sm md:text-base">
                {"7.5 - 9.0"}
              </label>
            </div>
          </li>
          <li className="flex items-center justify-between w-full">
            <div className="flex gap-2 items-center">
              <input
                type="checkbox"
                className="checked:accent-primary"
                checked={newFilters.matchScore === "9.0-10"}
                onChange={() => handleFilterChange("matchScore", "9.0-10")}
              />
              <label className="font-satoshi text-sm md:text-base">
                {"9.0 - 10.0"}
              </label>
            </div>
          </li>
        </ul>
      </div>
      <div className="flex gap-4 items-center self-end mt-4">
        <button
          onClick={handleReset}
          className="gap-1 flex items-center font-satoshi text-primary text-sm md:text-base font-medium p-1.5 md:p-2.5 bg-[#F1F0FA] rounded-xl"
        >
          <img src={reset} alt="reset" className="w-4 md:w-full" />
          Reset
        </button>
        <button
          onClick={handleApplyFilters}
          className="bg-primary text-white flex gap-1 items-center text-sm md:text-base p-1.5 md:p-2.5 font-satoshi font-medium rounded-xl"
        >
          <img src={tick} alt="tick" className="w-4 md:w-full" />
          Apply filters
        </button>
      </div>
    </div>
  );
}

export default FilterModal;
