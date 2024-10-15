# define _CRT_SECURE_NO_WARNINGS
# include <stdio.h>
# include <math.h>

int main()
{
	int YEAR = 0, MONTH = 0, DAY, LASTYEAR = 0, i;
	int AGE = 0;
	int QYEAR = 0; //QYEAR : 현재 년도
	int LASTQYEAR=0; //LASTQYEAR : 작년 년도
	int OPTION, DEC; //DEC : 생일 전년도의 12월 31일의 요일을 나타낸 MOD값
	int QDEC; //QDEC : 작년 년도의 12월 31일의 요일을 나타낸 MOD값
	int TOTALDAY = 0;
	int FEB; //FEB : 특정 년의 2월 달의 일수
	int PMOD; //PMOD : 생년의 첫날부터 생일까지의 일수의 MOD값
	int MOD; //DEC + PMOD의 MOD값
	int QMOD; //QDEC + PMOD의 MOD값
	int ALLDAY = 1; //1년 1월 1일부터 생년 1월 1일까지의 일수
	int MONTHDAY = 0; //특정 달의 총 일수
	if (MONTH == 2 && (YEAR % 400 == 0 || YEAR % 4 == 0 || QYEAR % 400 == 0 || QYEAR % 4 == 0)) FEB = 29;
	else if (MONTH == 2 && (YEAR % 100 == 0 || QYEAR % 100 == 0)) FEB = 28;
	else FEB = 28;
	int num = 0;
	int STARTDAY = 0;
	


	printf("Please enter a person's birth date (yyyy mm dd). Valid input range for the year entry is 0000 ~ 2020 :  ");
	scanf("%d %d %d", &YEAR, &MONTH, &DAY);
	while (YEAR < 0000 || YEAR > 2020 || MONTH < 1 || MONTH > 12 || DAY < 1 || DAY > 31) {
		printf("Please input valid range.\n");
		printf("Please enter a person’s birth date (yyyy mm dd). Valid input range for the year entry is 0000 ~ 2020 :  ");
		scanf("%d %d %d", &YEAR, &MONTH, &DAY);
	}

	printf("********************************************************************\n");
	printf("1. Display the day of the week when the person was born\n");
	printf("2. Display the day of the week on person’s nnth birthday\n");
	printf("3. Display the birth month calendar of the birth year\n");
	printf("4. Display the birth month calendar of the person’s nnth birthday\n");
	printf("********************************************************************\n");
	printf("Please enter your option (1 ~ 4): ");
	scanf("%d", &OPTION);

	switch (OPTION) {
	case 1:
		printf("Display the day of the week when the person was born\n");
		LASTYEAR = YEAR - 1;
		DEC = (LASTYEAR * 365 + (LASTYEAR / 4) - (LASTYEAR / 100) + (LASTYEAR / 400)) % 7;
		switch (MONTH) {
		case 1: TOTALDAY += DAY; break;
		case 2: TOTALDAY += DAY + 31; break;
		case 3: TOTALDAY += DAY + 31 + FEB; break;
		case 4: TOTALDAY += DAY + 31 + FEB + 31; break;
		case 5: TOTALDAY += DAY + 31 + FEB + 31 + 30; break;
		case 6: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31; break;
		case 7: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30; break;
		case 8: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31; break;
		case 9: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31; break;
		case 10: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30; break;
		case 11: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31; break;
		case 12: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30; break;
		}
		PMOD = TOTALDAY % 7;
		MOD = (DEC + PMOD) % 7;

		switch (MOD) {
		case 0: printf("This person was born on Sunday."); break;
		case 1: printf("This person was born on Monday."); break;
		case 2: printf("This person was born on Tuesday."); break;
		case 3: printf("This person was born on Wednesday."); break;
		case 4: printf("This person was born on Thursday."); break;
		case 5: printf("This person was born on Friday."); break;
		case 6: printf("This person was born on Saturday."); break;
		}
		break;
	case 2:
		printf("Display the day of the week on person’s nnth birthday\n");
		printf("Please enter a desired age. The valid range for the age is 0~120 :  ");
		scanf("%d", &AGE);
		while (AGE < 0 || AGE>120) {
			printf("Please input valid range.\n");
			printf("Please enter a desired age. The valid range for the age is 0~120 :  ");
			scanf("%d", &AGE);
		}
		QYEAR = YEAR + AGE - 1;
		LASTQYEAR = QYEAR - 1;
		QDEC = (LASTQYEAR * 365 + (LASTQYEAR / 4) - (LASTQYEAR / 100) + (LASTQYEAR / 400)) % 7;
		switch (MONTH) {
		case 1: TOTALDAY += DAY; break;
		case 2: TOTALDAY += DAY + 31; break;
		case 3: TOTALDAY += DAY + 31 + FEB; break;
		case 4: TOTALDAY += DAY + 31 + FEB + 31; break;
		case 5: TOTALDAY += DAY + 31 + FEB + 31 + 30; break;
		case 6: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31; break;
		case 7: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30; break;
		case 8: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31; break;
		case 9: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31; break;
		case 10: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30; break;
		case 11: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31; break;
		case 12: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30; break;
		}
		PMOD = TOTALDAY % 7;
		QMOD = (QDEC + PMOD) % 7;

		switch (QMOD) 
		case 0: printf("This person's %dth birthday is on Sunday.", AGE); break;
		case 1: printf("This person's %dth birthday is on Monday.", AGE); break;
		case 2: printf("This person's %dth birthday is on Tuesday.", AGE); break;
		case 3: printf("This person's %dth birthday is on Wednesday.", AGE); break;
	
		case 4: printf("This person's %dth birthday is on Thursday.", AGE); break;
		case 5: printf("This person's %dth birthday is on Friday.", AGE); break;
		case 6: printf("This person's %dth birthday is on Saturday.", AGE); break;
		}
		break;
	case 3: {
		printf("Display the birth month calendar of the birth year\n");
		printf("Year %d\n", YEAR);
		switch (MONTH) {
		case 1: printf("January\n"); break;
		case 2: printf("February\n"); break;
		case 3: printf("March\n"); break;
		case 4: printf("April\n"); break;
		case 5: printf("May\n"); break;
		case 6: printf("June\n"); break;
		case 7: printf("July\n"); break;
		case 8: printf("August\n"); break;
		case 9: printf("September\n"); break;
		case 10: printf("October\n"); break;
		case 11: printf("November\n"); break;
		case 12: printf("December\n"); break;
		}
		printf("\tSUN\tMON\tTUE\tWED\tTHU\tFRI\tSAT\n");
		ALLDAY = LASTYEAR * 365 + (LASTYEAR / 4) - (LASTYEAR / 100) + (LASTYEAR / 400);
		switch (MONTH) {
		case 1: TOTALDAY += DAY; break;
		case 2: TOTALDAY += DAY + 31; break;
		case 3: TOTALDAY += DAY + 31 + FEB; break;
		case 4: TOTALDAY += DAY + 31 + FEB + 31; break;
		case 5: TOTALDAY += DAY + 31 + FEB + 31 + 30; break;
		case 6: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31; break;
		case 7: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30; break;
		case 8: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31; break;
		case 9: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31; break;
		case 10: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30; break;
		case 11: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31; break;
		case 12: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30; break;
		}
		ALLDAY += TOTALDAY;
		int STARTDAY = ALLDAY % 7;
		for (i = 0; i < STARTDAY; i++) {
			printf("\t");
		}
		switch (MONTH) {
		case 1: MONTHDAY = 31; break;
		case 2: MONTHDAY = FEB; break;
		case 3: MONTHDAY = 31; break;
		case 4: MONTHDAY = 30; break;
		case 5: MONTHDAY = 31; break;
		case 6: MONTHDAY = 30; break;
		case 7: MONTHDAY = 31; break;
		case 8: MONTHDAY = 31; break;
		case 9: MONTHDAY = 30; break;
		case 10: MONTHDAY = 31; break;
		case 11: MONTHDAY = 30; break;
		case 12: MONTHDAY = 31; break;
		}
		for (int j = 1; j <= MONTHDAY; j++) {
			printf("%8d", j);
			if ((j + STARTDAY) % 7 == 0) {
				printf("\n");
			}
		}
		printf("Please enter '-1' for previous month, '1'for next month, and '0'for stop displaying :  ");
		scanf("%d", num);
		switch (num) {
		case -1: printf("Year %d\n", YEAR);
			switch (MONTH - 1) {
			case 1: printf("January\n"); break;
			case 2: printf("February\n"); break;
			case 3: printf("March\n"); break;
			case 4: printf("April\n"); break;
			case 5: printf("May\n"); break;
			case 6: printf("June\n"); break;
			case 7: printf("July\n"); break;
			case 8: printf("August\n"); break;
			case 9: printf("September\n"); break;
			case 10: printf("October\n"); break;
			case 11: printf("November\n"); break;
			case 12: printf("December\n"); break;
			}
			printf("\tSUN\tMON\tTUE\tWED\tTHU\tFRI\tSAT\n");
			ALLDAY = LASTYEAR * 365 + (LASTYEAR / 4) - (LASTYEAR / 100) + (LASTYEAR / 400);
			switch (MONTH - 1) {
			case 1: TOTALDAY += DAY; break;
			case 2: TOTALDAY += DAY + 31; break;
			case 3: TOTALDAY += DAY + 31 + FEB; break;
			case 4: TOTALDAY += DAY + 31 + FEB + 31; break;
			case 5: TOTALDAY += DAY + 31 + FEB + 31 + 30; break;
			case 6: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31; break;
			case 7: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30; break;
			case 8: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31; break;
			case 9: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31; break;
			case 10: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30; break;
			case 11: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31; break;
			case 12: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30; break;
			}
			ALLDAY += TOTALDAY;
			for (i = 0; i < STARTDAY; i++) {
				printf("\t");
			}
			switch (MONTH) {
			case 1: MONTHDAY = 31; break;
			case 2: MONTHDAY = FEB; break;
			case 3: MONTHDAY = 31; break;
			case 4: MONTHDAY = 30; break;
			case 5: MONTHDAY = 31; break;
			case 6: MONTHDAY = 30; break;
			case 7: MONTHDAY = 31; break;
			case 8: MONTHDAY = 31; break;
			case 9: MONTHDAY = 30; break;
			case 10: MONTHDAY = 31; break;
			case 11: MONTHDAY = 30; break;
			case 12: MONTHDAY = 31; break;
			}
			for (int j = 1; j <= MONTHDAY; j++) {
				printf("%8d", j);
				if ((j + STARTDAY) % 7 == 0) {
					printf("\n");
				}
			}
			break;
		case 0: printf("Program Terminated."); break;
		case 1: printf("Year %d\n", YEAR);
			switch (MONTH + 1) {
			case 1: printf("January\n"); break;
			case 2: printf("February\n"); break;
			case 3: printf("March\n"); break;
			case 4: printf("April\n"); break;
			case 5: printf("May\n"); break;
			case 6: printf("June\n"); break;
			case 7: printf("July\n"); break;
			case 8: printf("August\n"); break;
			case 9: printf("September\n"); break;
			case 10: printf("October\n"); break;
			case 11: printf("November\n"); break;
			case 12: printf("December\n"); break;
			}
			printf("\tSUN\tMON\tTUE\tWED\tTHU\tFRI\tSAT\n");
			ALLDAY = LASTYEAR * 365 + (LASTYEAR / 4) - (LASTYEAR / 100) + (LASTYEAR / 400);
			switch (MONTH + 1) {
			case 1: TOTALDAY += DAY; break;
			case 2: TOTALDAY += DAY + 31; break;
			case 3: TOTALDAY += DAY + 31 + FEB; break;
			case 4: TOTALDAY += DAY + 31 + FEB + 31; break;
			case 5: TOTALDAY += DAY + 31 + FEB + 31 + 30; break;
			case 6: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31; break;
			case 7: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30; break;
			case 8: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31; break;
			case 9: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31; break;
			case 10: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30; break;
			case 11: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31; break;
			case 12: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30; break;
			}
			ALLDAY += TOTALDAY;
			for (i = 0; i < STARTDAY; i++) {
				printf("\t");
			}
			switch (MONTH) {
			case 1: MONTHDAY = 31; break;
			case 2: MONTHDAY = FEB; break;
			case 3: MONTHDAY = 31; break;
			case 4: MONTHDAY = 30; break;
			case 5: MONTHDAY = 31; break;
			case 6: MONTHDAY = 30; break;
			case 7: MONTHDAY = 31; break;
			case 8: MONTHDAY = 31; break;
			case 9: MONTHDAY = 30; break;
			case 10: MONTHDAY = 31; break;
			case 11: MONTHDAY = 30; break;
			case 12: MONTHDAY = 31; break;
			}
			for (int j = 1; j <= MONTHDAY; j++) {
				printf("%8d", j);
				if ((j + STARTDAY) % 7 == 0) {
					printf("\n");
				}
			}
		}
		break;
	}
	case 4: {
			printf("Display the birth month calendar of the person’s nnth birthday\n");
			printf("Please enter a desired age. The valid range for the age is 0~120 :  ");
			scanf("%d", &AGE);
			while (AGE < 0 || AGE>120) {
				printf("Please input valid range.\n");
				printf("Please enter a desired age. The valid range for the age is 0~120 :  ");
				scanf("%d", &AGE);
			}
			printf("Year %d\n", QYEAR);
			switch (MONTH) {
			case 1: printf("January\n"); break;
			case 2: printf("February\n"); break;
			case 3: printf("March\n"); break;
			case 4: printf("April\n"); break;
			case 5: printf("May\n"); break;
			case 6: printf("June\n"); break;
			case 7: printf("July\n"); break;
			case 8: printf("August\n"); break;
			case 9: printf("September\n"); break;
			case 10: printf("October\n"); break;
			case 11: printf("November\n"); break;
			case 12: printf("December\n"); break;
			}
			printf("\tSUN\tMON\tTUE\tWED\tTHU\tFRI\tSAT\n");
			int QALLDAY;
			QALLDAY = LASTQYEAR * 365 + (LASTQYEAR / 4) - (LASTQYEAR / 100) + (LASTQYEAR / 400);
			switch (MONTH) {
			case 1: TOTALDAY += DAY; break;
			case 2: TOTALDAY += DAY + 31; break;
			case 3: TOTALDAY += DAY + 31 + FEB; break;
			case 4: TOTALDAY += DAY + 31 + FEB + 31; break;
			case 5: TOTALDAY += DAY + 31 + FEB + 31 + 30; break;
			case 6: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31; break;
			case 7: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30; break;
			case 8: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31; break;
			case 9: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31; break;
			case 10: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30; break;
			case 11: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31; break;
			case 12: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30; break;
			}
			QALLDAY += TOTALDAY;
			int QSTARTDAY = QALLDAY % 7;
			for (i = 0; i < QSTARTDAY; i++) {
				printf("\t");
			}
			switch (MONTH) {
			case 1: MONTHDAY = 31; break;
			case 2: MONTHDAY = FEB; break;
			case 3: MONTHDAY = 31; break;
			case 4: MONTHDAY = 30; break;
			case 5: MONTHDAY = 31; break;
			case 6: MONTHDAY = 30; break;
			case 7: MONTHDAY = 31; break;
			case 8: MONTHDAY = 31; break;
			case 9: MONTHDAY = 30; break;
			case 10: MONTHDAY = 31; break;
			case 11: MONTHDAY = 30; break;
			case 12: MONTHDAY = 31; break;
			}
			for (int j = 1; j <= MONTHDAY; j++) {
				printf("%8d", j);
				if ((j + STARTDAY) % 7 == 0) {
					printf("\n");
				}
			}
			printf("Please enter '-1' for previous month, '1'for next month, and '0'for stop displaying :  ");
			scanf("%d", num);
			switch (num) {
			case -1: printf("Year %d\n", YEAR);
				switch (MONTH - 1) {
				case 1: printf("January\n"); break;
				case 2: printf("February\n"); break;
				case 3: printf("March\n"); break;
				case 4: printf("April\n"); break;
				case 5: printf("May\n"); break;
				case 6: printf("June\n"); break;
				case 7: printf("July\n"); break;
				case 8: printf("August\n"); break;
				case 9: printf("September\n"); break;
				case 10: printf("October\n"); break;
				case 11: printf("November\n"); break;
				case 12: printf("December\n"); break;
				}
				printf("\tSUN\tMON\tTUE\tWED\tTHU\tFRI\tSAT\n");
				ALLDAY = LASTYEAR * 365 + (LASTYEAR / 4) - (LASTYEAR / 100) + (LASTYEAR / 400);
				switch (MONTH - 1) {
				case 1: TOTALDAY += DAY; break;
				case 2: TOTALDAY += DAY + 31; break;
				case 3: TOTALDAY += DAY + 31 + FEB; break;
				case 4: TOTALDAY += DAY + 31 + FEB + 31; break;
				case 5: TOTALDAY += DAY + 31 + FEB + 31 + 30; break;
				case 6: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31; break;
				case 7: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30; break;
				case 8: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31; break;
				case 9: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31; break;
				case 10: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30; break;
				case 11: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31; break;
				case 12: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30; break;
				}
				ALLDAY += TOTALDAY;
				for (i = 0; i < STARTDAY; i++) {
					printf(" ");
				}
				switch (MONTH) {
				case 1: MONTHDAY = 31; break;
				case 2: MONTHDAY = FEB; break;
				case 3: MONTHDAY = 31; break;
				case 4: MONTHDAY = 30; break;
				case 5: MONTHDAY = 31; break;
				case 6: MONTHDAY = 30; break;
				case 7: MONTHDAY = 31; break;
				case 8: MONTHDAY = 31; break;
				case 9: MONTHDAY = 30; break;
				case 10: MONTHDAY = 31; break;
				case 11: MONTHDAY = 30; break;
				case 12: MONTHDAY = 31; break;
				}
				for (int j = 1; j <= MONTHDAY; j++) {
					printf("%8d", j);
					if ((j + STARTDAY) % 7 == 0) {
						printf("\n");
					}
				}
				break;
			case 0: printf("Program Terminated."); break;
			case 1: printf("Year %d\n", YEAR);
				switch (MONTH + 1) {
				case 1: printf("January\n"); break;
				case 2: printf("February\n"); break;
				case 3: printf("March\n"); break;
				case 4: printf("April\n"); break;
				case 5: printf("May\n"); break;
				case 6: printf("June\n"); break;
				case 7: printf("July\n"); break;
				case 8: printf("August\n"); break;
				case 9: printf("September\n"); break;
				case 10: printf("October\n"); break;
				case 11: printf("November\n"); break;
				case 12: printf("December\n"); break;
				}
				printf("\tSUN\tMON\tTUE\tWED\tTHU\tFRI\tSAT\n");
				ALLDAY = LASTYEAR * 365 + (LASTYEAR / 4) - (LASTYEAR / 100) + (LASTYEAR / 400);
				switch (MONTH + 1) {
				case 1: TOTALDAY += DAY; break;
				case 2: TOTALDAY += DAY + 31; break;
				case 3: TOTALDAY += DAY + 31 + FEB; break;
				case 4: TOTALDAY += DAY + 31 + FEB + 31; break;
				case 5: TOTALDAY += DAY + 31 + FEB + 31 + 30; break;
				case 6: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31; break;
				case 7: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30; break;
				case 8: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31; break;
				case 9: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31; break;
				case 10: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30; break;
				case 11: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31; break;
				case 12: TOTALDAY += DAY + 31 + FEB + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30; break;
				}
				ALLDAY += TOTALDAY;
				for (i = 0; i < STARTDAY; i++) {
					printf("\t");
				}
				switch (MONTH) {
				case 1: MONTHDAY = 31; break;
				case 2: MONTHDAY = FEB; break;
				case 3: MONTHDAY = 31; break;
				case 4: MONTHDAY = 30; break;
				case 5: MONTHDAY = 31; break;
				case 6: MONTHDAY = 30; break;
				case 7: MONTHDAY = 31; break;
				case 8: MONTHDAY = 31; break;
				case 9: MONTHDAY = 30; break;
				case 10: MONTHDAY = 31; break;
				case 11: MONTHDAY = 30; break;
				case 12: MONTHDAY = 31; break;
				}
				for (int j = 1; j <= MONTHDAY; j++) {
					printf("%8d", j);
					if ((j + STARTDAY) % 7 == 0) {
						printf("\n");
					}
				}
			}
			break;
		}
		return 0;
	default: { {printf("Please input valid value."); }}
	}
	return 0;
}
			
			
	

	
		
