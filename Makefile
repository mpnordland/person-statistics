
dist:
	poetry run pytest
	poetry build

clean:

	- rm -r ./dist