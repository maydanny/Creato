# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Node Requirements

You must have npm globally installed on your computer. Please check the [Node version manager](https://github.com/nvm-sh/nvm) for installation details.

## Installing Yarn

```
npm install -g yarn
```

This will globally install yarn in your computer. You will be able to use yarn in any directories.

## Available Scripts

In the project directory, you can run:

### `yarn start` or `make dev_env`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `yarn build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `make prod`

It will run the linter on the client side code and run tests. After finishing the tests, it will automatically save and push the commits to this repository. It will also automatically deploy to Heroku.