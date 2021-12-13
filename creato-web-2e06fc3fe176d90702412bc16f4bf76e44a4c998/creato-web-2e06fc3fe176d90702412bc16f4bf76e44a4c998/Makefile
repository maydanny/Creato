FORCE:

tests: FORCE
	npx eslint --fix

prod: tests
	git add .
	git commit -am "Make prod command"
	git push origin master

dev_env: FORCE
	yarn install
	yarn start