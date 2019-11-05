import React from "react"

import {createStore, applyMiddleware, compose} from "redux"
import reducer from "./reducers"
import thunk from "redux-thunk"
import logger from "redux-logger"
import persistState from "redux-localstorage"

// import {fetchProjects} from "./actions.js"

export function configureStore(initialState = undefined) {
  let store = createStore(
    reducer,
    initialState,
    compose(
      persistState(),
      applyMiddleware(thunk, logger)
    )
  )

  if (module.hot) {
    module.hot.accept(() => {
      let reducer = require("./reducers").default
      store.replaceReducer(reducer)
    })
  }

  // dispatch action to fetch initial data
  // store.dispatch(fetchProjects("kal"))

  return store
}
