import { NavLink } from "react-router-dom";
import { ProfileButton } from "./ProfileButton.tsx";
import "./Navigation.css";

function Navigation() {
  return (
    <ul>
      <li>
        <NavLink to="/">Home</NavLink>
      </li>

      <li>
        <ProfileButton />
      </li>
    </ul>
  );
}

export { Navigation };
