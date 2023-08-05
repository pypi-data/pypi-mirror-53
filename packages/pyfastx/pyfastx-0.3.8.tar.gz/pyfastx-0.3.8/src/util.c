#include "util.h"

//check file is whether exists in disk
uint16_t file_exists(char *file_name){
	FILE *file;
	if((file = fopen(file_name, "r"))){
		fclose(file);
		return 1;
	}
	return 0;
}

void remove_space(char *str) {
	uint32_t i, j = 0;
	for(i = 0; str[i]; i++){
		if(!isspace(str[i])){
			str[j++] = str[i];
		}
	}
	str[j] = '\0';
}

void upper_string(char *str) {
	uint32_t i;
	for(i = 0; str[i]; i++) {
		if(str[i] >= 'a' && str[i] <= 'z'){
			str[i] = str[i] - 32;
		}
	}
}

void reverse_seq(char *seq){
	char *p1, *p2;

	if (! seq || ! *seq){
		return;
	}
	for (p1 = seq, p2 = seq + strlen(seq) - 1; p2 > p1; ++p1, --p2){
		*p1 ^= *p2;
		*p2 ^= *p1;
		*p1 ^= *p2;
	}
}

void complement_seq(char *seq){
	uint32_t i;

	for(i=0; seq[i]; i++){
		switch(seq[i]){
			case 65:
				seq[i]=84; break;
			
			case 67:
				seq[i]=71; break;
			
			case 71:
				seq[i]=67; break;
			
			case 84:
				seq[i]=65; break;

			case 97:
				seq[i]=116; break;

			case 99:
				seq[i]=103; break;

			case 103:
				seq[i]=99; break;

			case 116:
				seq[i]=97; break;
		}
	}
}

PyObject *clean_seq(PyObject *self, PyObject *args){
	char *seq;
	if (!PyArg_ParseTuple(args, "s", &seq)){
		return NULL;
	}
	uint32_t i;
	uint32_t j = 0;
	for(i=0; seq[i]; i++){
		if(!isspace(seq[i])){
			seq[j++] = toupper(seq[i]);
		}
	}
	seq[j] = '\0';
	return Py_BuildValue("s", seq);
}

void truncate_seq(char *seq, uint32_t start, uint32_t end){
	uint32_t len;
	uint32_t i = 0;
	uint32_t j = 0;
	len = end - start + 1;

	for(i=0; i<strlen(seq); i++){
		if(isspace(seq[i])){
			continue;
		}

		seq[j++] = toupper(seq[i]);

		if(j > len){
			break;
		}
	}
	seq[j] = '\0';
}


PyObject *sub_seq(PyObject *self, PyObject *args){
	char *seq;
	uint32_t start;
	uint32_t end;

	if (!PyArg_ParseTuple(args, "sii", &seq, &start, &end)){
		return NULL;
	}
	uint32_t i;
	uint32_t j = 0;
	uint32_t real_pos = 0;
	uint16_t flag;
	for(i=0; seq[i]; i++){
		flag = isspace(seq[i]);

		if(!flag){
			real_pos++;
		}

		if(real_pos > end){
			break;
		}

		if(real_pos >= start){
			if(!flag){
				seq[j++] = toupper(seq[i]);
			}
		}
	}
	seq[j] = '\0';
	return Py_BuildValue("s", seq);
}

/*check input file is whether gzip file
@para file_name str, input file path string
@return bool, 1 is gzip formmat file, 0 is not gzip
*/
uint16_t is_gzip_format(char* file_name){
	uint16_t ret;
	FILE* fd;
	unsigned char magic[4] = {0};

	fd = fopen(file_name, "rb");
	ret = fread(magic, 1, sizeof(magic), fd);
	fclose(fd);

	if(ret != sizeof(magic)){
		return 0;
	}
	
	if(magic[0] != 0x1f || magic[1] != 0x8b || magic[2] != 0x08){
		return 0;
	}
	
	return 1;
}
