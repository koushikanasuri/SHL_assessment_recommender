from recommend import recommend

res = recommend("Java developer with teamwork skills")
for r in res:
    print(r["url"])