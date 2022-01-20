all:
	cd bio && python3 ../code/python/index.py . --e --h Biographies
	cd events && python3 ../code/python/index.py . --e --h Events

git:
	git add .
	git commit -m "Make initiated commit"
	git push
