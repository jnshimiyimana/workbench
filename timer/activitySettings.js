import React from "react"

import {COLORS} from "./colors.js"
import {gettext} from "./i18n.js"

export const ActivitySettings = ({
  color,
  setColor,
  removeActivity,
  resetActivity,
}) => (
  <div className="activity-settings">
    <div className="activity-color-chooser">
      {COLORS.map((c) => (
        <label
          key={c}
          className={c == color ? "checked" : ""}
          style={{backgroundColor: c}}
        >
          <input
            type="radio"
            name="color"
            value={c}
            onClick={() => setColor(c)}
          />
        </label>
      ))}
    </div>
    <div className="d-flex mt-3 justify-content-between">
      <button
        className="btn btn-danger"
        type="button"
        onClick={() => removeActivity()}
      >
        {gettext("Remove")}
      </button>
      <button
        className="btn btn-warning"
        type="button"
        onClick={() => resetActivity()}
      >
        {gettext("Reset")}
      </button>
    </div>
  </div>
)