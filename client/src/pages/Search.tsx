import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { TALENTS, TalentType } from "../store/data";
import Footer from "../components/Footer";
import ReactPaginate from "react-paginate";
import { getExperience, getMatchScore } from "../utils/filters";
import SearchHeader from "../components/Search/SearchHeader";
import useStore from "../store";
import ModalLayout from "../components/ModalLayout";
import Hero from "../components/Search/Hero";

function Search() {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const queryParamValue = searchParams.get("q");

  const [talents, setTalents] = useState<TalentType[]>([]);
  const [searchText, setSearchText] = useState(queryParamValue || "");
  const [filters, setFilters] = useState<{ [key: string]: string }>({
    experience: "",
    matchScore: "",
  });

  //pagination logic
  const itemsPerPage = 10;
  const [currentPage, setCurrentPage] = useState(0);
  const pageCount = Math.ceil(talents.length / itemsPerPage);

  const handlePageChange = ({ selected }: { selected: any }) => {
    setCurrentPage(selected);
  };
  const displayedData = talents.slice(
    currentPage * itemsPerPage,
    (currentPage + 1) * itemsPerPage
  );

  useEffect(() => {
    let filteredTalents = TALENTS.filter((talent) => {
      if (filters.experience) {
        const [min, max] = getExperience(filters.experience);
        if (talent.experience < min || talent.experience > max) return false;
      }
      if (filters.matchScore) {
        const [min, max] = getMatchScore(filters.matchScore);
        if (talent.score < min || talent.score > max) return false;
      }
      return true;
    });
    if (searchText) {
      filteredTalents = filteredTalents.filter((talent) =>
        talent.expertise.toLowerCase().includes(searchText.toLowerCase())
      );
    } else {
      filteredTalents = filteredTalents
        .sort(() => 0.5 - Math.random())
        .slice(0, 10);
      setTalents(filteredTalents);
    }

    setTalents(filteredTalents);
  }, [filters]);

  const { currentModal } = useStore();

  useEffect(() => {
    if (currentModal != null) document.body.style.overflow = "hidden";
    else document.body.style.overflow = "";
  }, [currentModal]);

  return (
    <div className="bg-[#E2E1EC] w-screen h-screen overflow-x-hidden">
      {currentModal && <ModalLayout />}
      <div className="max-w-screen-2xl min-h-[80vh] mx-auto p-4 md:p-8">
        <SearchHeader searchText={searchText} setSearchText={setSearchText} />
        <Hero
          talents={displayedData}
          setFilters={setFilters}
          filters={filters}
          queryParamValue={queryParamValue}
        />
      </div>
      <ReactPaginate
        previousLabel={""}
        nextLabel={""}
        breakLabel={"..."}
        pageCount={pageCount}
        marginPagesDisplayed={2}
        pageRangeDisplayed={2}
        onPageChange={handlePageChange}
        pageClassName="block cursor-pointer"
        containerClassName="flex justify-center items-center font-medium mt-12 gap-5"
        activeClassName=""
      />
      <Footer />
    </div>
  );
}

export default Search;
