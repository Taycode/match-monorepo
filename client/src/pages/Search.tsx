import { useLocation } from "react-router-dom";

function Search() {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const queryParamValue = searchParams.get("q");
  return (
    <div>
      <h1>Search</h1>
      <p>{queryParamValue}</p>
    </div>
  );
}

export default Search;
